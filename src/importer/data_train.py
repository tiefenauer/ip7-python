import logging
import sys

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class TrainingData(object):
    def __init__(self, id):
        self.id = id
        if self.id is None:
            self.id = -1000

    def __enter__(self):
        self.conn_read = db.connect_to(Database.X28)
        self.conn_write = db.connect_to(Database.X28)
        cursor = self.conn_read.cursor()
        cursor.execute("""SELECT count(*) AS num_rows 
                          FROM labeled_jobs 
                          WHERE %(id)s < 0 OR id = %(id)s""",
                       {'id': self.id})
        self.num_rows = cursor.fetchone()['num_rows']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_read.close()
        self.conn_write.close()

    def __iter__(self):
        cursor = self.conn_read.cursor()
        cursor.execute("""SELECT id, html, plaintext, url, title, x28_id 
                          FROM labeled_jobs
                          WHERE %(id)s < 0 OR id = %(id)s
                          """,
                       {'id': self.id}
                       )
        for row in cursor:
            yield row

    def classify_job(self, job_id, job_name, job_count):
        cursor = self.conn_write.cursor()
        cursor.execute("""INSERT INTO job_name_fts (job_id, job_name, job_count) 
                          VALUES(%s, %s, %s)""",
                       (job_id, job_name, job_count))
        self.conn_write.commit()

    def truncate_classification_tables(self):
        logging.info('truncating target tables...')
        cursor = self.conn_read.cursor()
        cursor.execute("""TRUNCATE job_name_fts""")
        self.conn_read.commit()
