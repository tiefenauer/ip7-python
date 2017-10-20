import logging
import sys

import pandas
from tqdm import tqdm

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class FetchflowImporter(object):

    def __enter__(self):
        self.conn_read = db.connect_to(Database.FETCHFLOW)
        self.conn_write = db.connect_to(Database.FETCHFLOW)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_read.close()

    def __iter__(self):
        cursor = self.conn_read.cursor(dictionary=True)
        cursor.execute("SELECT count(*) AS num_total FROM labeled_text")
        num_total = cursor.fetchone()['num_total']
        logging.info('processing {} rows'.format(num_total))

        cursor.execute("SELECT id, title, contentbytes AS dom FROM labeled_text")
        for row in tqdm(cursor, total=num_total, unit=' rows'):
            yield row

    def update_job(self, row, match):
        if match is not None:
            labeled_text_id = row['id']
            job_title = match['job_name']
            job_title_count = len(match['job_contexts'])
            cursor = self.conn_write.cursor()
            sql = """INSERT INTO job_titles (labeled_text_id, job_title, job_title_count) 
                        VALUES (%s, %s, %s) 
                        ON DUPLICATE KEY UPDATE 
                        job_title = VALUES(job_title),
                        job_title_count = VALUES(job_title_count)
          """
            cursor.execute(sql, (labeled_text_id, job_title, job_title_count))
            self.conn_write.commit()




class JobNameImporter(object):
    def __init__(self):
        self.job_names = pandas.read_csv('../resource/tbfulljob_DE.tsv', delimiter=';', names=['job_name'])

    def __iter__(self):
        for job_name in self.job_names['job_name']:
            yield job_name