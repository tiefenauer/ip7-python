import logging
import sys
import time

import itertools
import pandas
from tqdm import tqdm

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class FetchflowImporter(object):
    def __init__(self):
        self.curr_datetime = time.strftime('%Y-%m-%d %H:%M:%S')

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

    def update_job_with_title(self, row, job_title):
        labeled_text_id = row['id']
        last_update = self.curr_datetime;
        cursor = self.conn_write.cursor()
        sql = """INSERT INTO job_titles (labeled_text_id, job_title, last_update) 
                    VALUES (%s, %s, %s) 
                    ON DUPLICATE KEY UPDATE 
                    job_title = VALUES(job_title),
                    last_update = VALUES(last_update)
        """
        cursor.execute(sql, (labeled_text_id, job_title, last_update))
        self.conn_write.commit()
        return cursor.lastrowid

    def update_job_contexts(self, job_title_id, matches):
        cursor = self.conn_write.cursor()
        for match in matches:
            # insert contexts
            for job_context in match['job_contexts']:
                cursor.execute("""INSERT INTO job_contexts (job_context, last_update) VALUES (%s, %s)""",
                               (job_context, self.curr_datetime))
                cursor.execute(
                    """INSERT INTO job_title_contexts (fk_job_title, fk_job_context, last_update) VALUES (%s, %s, %s)""",
                    (job_title_id, cursor.lastrowid, self.curr_datetime))
        self.conn_write.commit()

    def truncate_results(self):
        cursor = self.conn_write.cursor()
        cursor.execute("""TRUNCATE job_contexts""")
        cursor.execute("""TRUNCATE  job_title_contexts""")
        cursor.execute("""TRUNCATE job_titles""")
        self.conn_write.commit()


class JobNameImporter(object):
    def __init__(self):
        self.job_names = pandas.read_csv('../resource/job_titles.tsv', delimiter=';', names=['job_name'])

    def __iter__(self):
        for job_name in self.job_names['job_name']:
            yield job_name
