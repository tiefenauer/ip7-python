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

        cursor.execute("SELECT id, title, contentbytes AS dom FROM labeled_text WHERE has_job_title = 0")
        for row in tqdm(cursor, total=num_total, unit=' rows'):
            yield row

    def update_job(self, row, match):
        cursor = self.conn_write.cursor()
        cursor.execute("""UPDATE labeled_text set has_job_title=1, job_title=%s where id=%s""", (match['job_name'], row['id']))
        self.conn_write.commit()




class JobNameImporter(object):
    def __init__(self):
        self.job_names = pandas.read_csv('../resource/tbfulljob_DE.tsv', delimiter=';', names=['job_name'])

    def __iter__(self):
        for job_name in self.job_names['job_name']:
            yield job_name