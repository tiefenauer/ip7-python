import logging
import sys

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class TrainingData(object):
    def __init__(self, id=None, limit=1, offset=0):
        self.id = id
        self.split_from = offset
        self.split_to = limit
        if self.id is None:
            self.id = -1000

    def __enter__(self):
        self.conn_read = db.connect_to(Database.X28_PG)
        self.conn_write = db.connect_to(Database.X28_PG)
        cursor = self.conn_read.cursor()
        cursor.execute("""SELECT count(*) AS num_rows 
                          FROM data_train 
                          WHERE %(id)s < 0 OR id = %(id)s""",
                       {'id': self.id})
        self.num_total = cursor.fetchone()['num_rows']
        self.offset = int(self.num_total * self.split_from)
        self.limit = int(self.num_total * self.split_to)
        self.num_rows = self.limit - self.offset
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_read.close()
        self.conn_write.close()

    def __iter__(self):
        sql = """SELECT id, html, plaintext, url, title, x28_id 
                          FROM data_train
                          WHERE %(id)s < 0 OR id = %(id)s
                          """
        parms = {'id': self.id}
        sql, parms = self.limit_offset(sql, parms)

        cursor = self.conn_read.cursor()
        cursor.execute(sql, parms)
        for row in cursor:
            yield row

    def limit_offset(self, sql, parms):
        if self.split_from < 1:
            sql += ' OFFSET %(offset)s'
            parms['offset'] = self.offset  # 97204
        if self.split_to < 1:
            sql += ' LIMIT %(limit)s'
            parms['limit'] = self.limit  # 100
        return sql, parms

    def classify_job(self, job_id, job_name, score_strict, score_tolerant, score_linear):
        cursor = self.conn_write.cursor()
        cursor.execute("""INSERT INTO classification_result_fts (job_id, job_name, score_strict, score_tolerant, score_linear) 
                          VALUES(%s, %s, %s, %s, %s)""",
                       (job_id, job_name, score_strict, score_tolerant, score_linear))
        self.conn_write.commit()

    def truncate_classification_tables(self):
        logging.info('truncating target tables...')
        cursor = self.conn_read.cursor()
        cursor.execute("""TRUNCATE classification_result_fts""")
        self.conn_read.commit()
