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
        self.conn_read = db.connect_to(Database.X28_PG)
        self.conn_write = db.connect_to(Database.X28_PG)
        cursor = self.conn_read.cursor()
        cursor.execute("""SELECT count(*) AS num_rows 
                          FROM data_train 
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
                          FROM data_train
                          WHERE %(id)s < 0 OR id = %(id)s
                          """,
                       {'id': self.id}
                       )
        for row in cursor:
            yield row

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
