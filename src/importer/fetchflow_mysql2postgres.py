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
cur_mysql_r.execute("""SELECT count(*) AS num FROM labeled_text""")
num_rows = cur_mysql_r.fetchone()['num']
num_migrated = 0
num_non_migrateable = 0

logging.info('processing {} rows'.format(num_rows))

cur_pg = conn_pg.cursor()
cur_pg.execute("""TRUNCATE TABLE labeled_text""")
conn_pg.commit()

i = 0
batchsize = 1000
num_batches = math.ceil(num_rows / batchsize)
pbar = tqdm(total=num_rows, unit=' rows')
while i < num_batches:
    offset = i * batchsize
    limit = batchsize
    # use joined tables for performance reasons: paging with limit+ offset is very poor in MySQL!
    sql = """SELECT labeled_text.id, title, CONVERT(contentbytes USING utf8) AS html 
            FROM labeled_text
            JOIN ( SELECT id FROM labeled_text LIMIT %s, %s ) AS t ON t.id = labeled_text.id
            WHERE labeled_text.migrated = 0 and labeled_text.migrateable = 1
            """
    cur_mysql_r.execute(sql, (limit, offset))
    for row in cur_mysql_r:
        try:
            rowid = row['id']
            cur_pg.execute("""INSERT INTO labeled_text (fetchflow_id, html) 
                          VALUES (%s, %s)""", (rowid, row['html']))
            cur_mysql_w.execute("""UPDATE labeled_text SET migrated = 1 WHERE id={}""".format(rowid))
            conn_mysql_w.commit()
            num_migrated += 1
        except ValueError:
            logging.info('could not migrate row id={}'.format(rowid))
            cur_mysql_w.execute("""UPDATE labeled_text SET migrateable = 0 WHERE id={}""".format(rowid))
            conn_mysql_w.commit()
            num_non_migrateable += 1
    conn_pg.commit()
    pbar.update(batchsize)
    i += 1

logging.info('migrated {}/{} rows. Could not migrate {} rows'.format(num_migrated, num_rows, num_non_migrateable))
