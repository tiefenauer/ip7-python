import argparse
import logging
import math
import sys

from pony.orm import db_session, select, commit
from tqdm import tqdm

from src.database.entities_mysql_fetchflow import Labeled_Text
from src.database.entities_x28 import Fetchflow_HTML, pgdb

parser = argparse.ArgumentParser(description="""Migrate MySQL to PG""")
parser.add_argument('-t', '--truncate', type=bool, default=False,
                    help='(optional) truncate target table')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

num_migrated = num_non_migrateable = num_empty = num_not_html = 0
limit = 1000
with db_session:
    if args.truncate:
        logging.info('Truncating target tables...')
        Fetchflow_HTML.select().delete()
        pgdb.commit()
        logging.info('...done!')

    rowid = select(r.id for r in Labeled_Text).min()

    num_rows = Labeled_Text.select(lambda r: r.migrated == 0 and r.migrateable == 1).count()
    num_batches = int(math.ceil(num_rows / limit))
    for i in tqdm(range(0, num_batches), total=num_batches, unit=' rows', unit_scale=1000):
        cursor = Labeled_Text.select(lambda r: r.migrated == 0 and r.migrateable == 1 and r.id > rowid) \
                     .for_update() \
                     .order_by(Labeled_Text.id)[0:limit]
        for row in cursor:
            if row.contenttype and 'text/html' not in row.contenttype:
                num_not_html += 1
                continue
            if not row.html:
                num_empty += 1
                continue
            rowid = row.id
            try:
                html = False
                try:
                    html = row.html.decode(encoding='utf-8')
                except UnicodeError as e:
                    try:
                        html = row.html.decode(encoding='latin_1')
                    except ValueError as e:
                        num_non_migrateable += 1
                        logging.info("""could not decode html: {}""".format(str(e)))

                if html:
                    try:
                        Fetchflow_HTML(fetchflow_id=rowid, html=html)
                    except ValueError as e:
                        logging.info("could not write html: {}".format(str(e)))
                try:
                    row.migrated = 1
                    num_migrated += 1
                except Exception as e:
                    # rollback()
                    num_non_migrateable += 1
                    row.migrateable = 0
                    logging.info("""could not update migration status: {}""".format(str(e)))
            except Exception as e:
                # rollback()
                num_non_migrateable += 1
                logging.info('could not migrate row id={}: {}'.format(rowid, str(e)))
                try:
                    row.migrateable = 0
                except Exception as e:
                    # rollback()
                    logging.info('could not update migrateable status: {}'.format(str(e)))
        commit()
    logging.info('migrated {}/{} rows.'.format(num_migrated, num_rows))
    logging.info('Could not migrate {} rows. {} rows were empty. {} rows were not HTML'.format(num_non_migrateable,
                                                                                               num_empty, num_not_html))
