import logging
import math
import sys

from tqdm import tqdm

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

conn_mysql_r = db.connect_to(Database.FETCHFLOW_MYSQL)
conn_mysql_w = db.connect_to(Database.FETCHFLOW_MYSQL)
conn_pg = db.connect_to(Database.FETCHFLOW_PG)

cur_mysql_r = conn_mysql_r.cursor(dictionary=True)
cur_mysql_w = conn_mysql_w.cursor(dictionary=True)
cur_mysql_r.execute("""SELECT count(*) AS num FROM labeled_text where migrated = 0 and migrateable = 1""")
num_rows = cur_mysql_r.fetchone()['num']
num_migrated = 0
num_non_migrateable = 0
num_empty = 0

logging.info('processing {} rows'.format(num_rows))

cur_pg = conn_pg.cursor()
# cur_pg.execute("""TRUNCATE TABLE labeled_text""")
# conn_pg.commit()

i = 0
limit = 1000
num_batches = math.ceil(num_rows / limit)
pbar = tqdm(total=num_rows, unit=' rows')
rowid = -2
for i in range(0, num_batches):
    offset = i * limit
    # use joined tables for performance reasons: paging with limit+ offset is very poor in MySQL!
    sql = """SELECT labeled_text.id, title, CONVERT(contentbytes USING latin1) AS html 
            FROM labeled_text
            WHERE id > {} and labeled_text.migrated = 0 and labeled_text.migrateable = 1
            order by id
            limit 0, 1000
            """.format(rowid)
    cur_mysql_r.execute(sql)
    for row in cur_mysql_r:
        if not row['html']:
            num_empty += 1
            continue
        rowid = row['id']
        try:
            cur_pg.execute("""INSERT INTO labeled_text (fetchflow_id, html) 
                          VALUES (%s, %s)""", (rowid, row['html']))
            conn_pg.commit()
            try:
                cur_mysql_w.execute("""UPDATE labeled_text SET migrated = 1 WHERE id={}""".format(rowid))
                conn_mysql_w.commit()
                num_migrated += 1
            except Exception as e:
                num_non_migrateable += 1
                conn_mysql_w.rollback()
                logging.info("""could not update migration status: {}""".format(str(e)))
        except Exception as e:
            num_non_migrateable += 1
            conn_pg.rollback()
            logging.info('could not migrate row id={}: {}'.format(rowid, str(e)))
            try:
                num_non_migrateable += 1
                cur_mysql_w.execute("""UPDATE labeled_text SET migrateable = 0 WHERE id={}""".format(rowid))
                conn_mysql_w.commit()
            except Exception as e:
                conn_mysql_w.rollback()
                logging.info('could not update migrateable status: {}'.format(str(e)))
    conn_pg.commit()
    pbar.update(limit)

logging.info('migrated {}/{} rows. Could not migrate {} rows. {} rows were empty'.format(num_migrated, num_rows, num_non_migrateable, num_empty))
