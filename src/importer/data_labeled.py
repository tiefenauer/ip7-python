import logging
import sys

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class LabeledData(object):
    def __init__(self, id=None, split_from=0, split_to=1):
        self.id = id
        self.split_from = split_from
        self.split_to = split_to
        if self.id is None:
            self.id = -1000

    def __enter__(self):
        self.conn_read = db.connect_to(Database.X28)
        self.conn_write = db.connect_to(Database.X28)
        sql = """SELECT count(*) AS num_rows 
                                  FROM labeled_jobs 
                                  WHERE %(id)s < 0 OR id = %(id)s
                                  """
        parms = {'id': self.id}
        cursor = self.conn_read.cursor()
        cursor.execute(sql, parms)
        self.num_total = cursor.fetchone()['num_rows']
        self.offset = int(self.num_total * self.split_from)
        self.limit = int(self.num_total * self.split_to)

        self.num_rows = self.limit - self.offset
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_read.close()
        self.conn_write.close()

    def __iter__(self):
        cursor = self.conn_read.cursor()
        sql = """SELECT id, html, plaintext, url, title, x28_id 
                          FROM labeled_jobs
                          WHERE %(id)s < 0 OR id = %(id)s
                          """
        parms = {'id': self.id}
        sql, parms = self.limit_offset(sql, parms)
        cursor.execute(sql, parms)
        for row in cursor:
            yield row

    def limit_offset(self, sql, parms):
        if self.split_from < 1:
            sql += ' OFFSET %(offset)s'
            parms['offset'] = self.offset  # 97204
        if self.split_to < 1:
            sql += ' LIMIT %(limit)s'
            parms['limit'] = self.limit # 100
        return sql, parms

    def update_job_class(self, job_id, job_name):
        cursor = self.conn_write.cursor()
        cursor.execute("""INSERT INTO job_name_fts (job_id, job_name) 
                          VALUES(%s, %s)""",
                       (job_id, job_name))
        self.conn_write.commit()

    def truncate_target(self):
        logging.info('truncating target tables...')
        cursor = self.conn_read.cursor()
        cursor.execute("""TRUNCATE job_name_fts""")
        self.conn_read.commit()
