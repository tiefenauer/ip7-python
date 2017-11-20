import argparse
import logging
import math
import sys

from pony.orm import db_session, select
from tqdm import tqdm

from src.database.entities_mysql import Labeled_Text, mysql
from src.database.entities_pg import Fetchflow_HTML, pg

parser = argparse.ArgumentParser(description="""Migrate MySQL to PG""")
parser.add_argument('-t', '--truncate', type=bool, default=False,
                    help='(optional) truncate target table')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

num_migrated = num_non_migrateable = num_empty = 0
limit = 1000


def decode_html(row):
    html = None
    try:
        html = row.html.decode(encoding='utf-8')
    except UnicodeError as e:
        try:
            html = row.html.decode(encoding='latin_1')
        except ValueError as e:
            logging.info("""could not decode html: {}""".format(str(e)))
    return html


def update_migrateable(row, migrateable):
    try:
        row.migrateable = int(migrateable)
    except Exception as e:
        logging.info("""could not update labeled_text.migrateable: {}""".format(str(e)))
        return False
    return True


def update_migrated(row, migrated):
    try:
        row.migrated = int(migrated)
    except Exception as e:
        logging.info("""could not update labeled_text.migrated: {}""".format(str(e)))
        return False
    return True


def write_entity(html, row):
    ent = None
    try:
        ent = Fetchflow_HTML(fetchflow_id=row.id, html=html)
        pg.commit()
    except Exception as e:
        logging.info("could not write fetchflow_html: {}".format(str(e)))
    return ent


with db_session:
    if args.truncate:
        logging.info('Truncating target tables...')
        Fetchflow_HTML.select().delete()
        pg.commit()
        logging.info('...done!')

    rowid = select(r.id for r in Labeled_Text).min() - 1

    num_rows = Labeled_Text.select(lambda r: r.migrated == 0 and r.migrateable == 1).count()
    num_batches = int(math.ceil(num_rows / limit))
    for i in tqdm(range(0, num_batches), total=num_batches, unit=' rows', unit_scale=1000):
        cursor = Labeled_Text.select(lambda r: r.migrated == 0 and r.migrateable == 1 and r.id > rowid) \
                     .for_update() \
                     .order_by(Labeled_Text.id)[0:limit]
        for row in cursor:
            rowid = row.id

            html = decode_html(row)
            if not html:
                num_non_migrateable += 1
                update_migrateable(row, False)
                continue

            entity = write_entity(html, row)
            if not entity:
                num_non_migrateable += 1
                continue

            num_migrated += 1
            update_migrated(row, True)
        mysql.commit()
    logging.info('migrated {}/{} rows.'.format(num_migrated, num_rows))
    logging.info('Could not migrate {} rows due to charset errors'.format(num_non_migrateable))
    logging.info('Could not migrate {} rows because content was empty.'.format(num_empty))
