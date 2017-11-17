import logging
import sys
import time

from tqdm import tqdm

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class FetchflowImporter(object):
    def __init__(self, args):
        self.curr_datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.conn_read = db.connect_to(Database.FETCHFLOW_MYSQL)
        self.conn_write = db.connect_to(Database.FETCHFLOW_MYSQL)
        self.id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        self.split_from = args.offset if hasattr(args, 'offset') else 0
        self.split_to = args.limit if hasattr(args, 'limit') else 1
        cursor = self.conn_read.cursor(dictionary=True)
        cursor.execute("SELECT count(*) AS num_total FROM labeled_text")
        self.num_total = cursor.fetchone()['num_total']
        self.offset = int(self.num_total * self.split_from)
        self.limit = int(self.num_total * self.split_to)
        self.num_rows = self.limit - self.offset

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_read.close()
        self.conn_write.close()

    def __iter__(self):
        cursor = self.conn_read.cursor(dictionary=True)
        cursor.execute("SELECT id, title, CONVERT(contentbytes USING utf8) AS html FROM labeled_text LIMIT 1000")
        for row in cursor:
            yield Row(row)

    def update_job_with_title(self, row, job_title, job_count):
        labeled_text_id = row['id']
        last_update = self.curr_datetime;
        cursor = self.conn_write.cursor()
        sql = """INSERT INTO job_titles (labeled_text_id, job_title, job_count, last_update) 
                    VALUES (%s, %s, %s, %s) 
                    ON DUPLICATE KEY UPDATE 
                    job_count = VALUES(job_count),
                    job_title = VALUES(job_title),
                    last_update = VALUES(last_update)
        """
        cursor.execute(sql, (labeled_text_id, job_title, job_count, last_update))
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
        logging.info('Truncating target tables...')
        cursor = self.conn_write.cursor()
        cursor.execute("""TRUNCATE job_contexts""")
        cursor.execute("""TRUNCATE  job_title_contexts""")
        cursor.execute("""TRUNCATE job_titles""")
        self.conn_write.commit()


class Row(dict):
    def __init__(self, row):
        self.id = row['id']
        self.html = row['html']
