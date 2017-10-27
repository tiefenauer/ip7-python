import logging
import os
import sys

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class X28ImporterJson(object):
    def __init__(self, dirname='D:/db/x28'):
        self.dirname = dirname
        self.num_files = len([name for name in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, name))])

    def __enter__(self):
        self.conn_x28 = db.connect_to(Database.X28)
        self.conn_fetchflow = db.connect_to(Database.X28_FETCHFLOW)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_x28.close()
        self.conn_fetchflow.close()

    def __iter__(self):
        logging.info('Processing {} files...'.format(self.num_files))
        for fname in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, fname), encoding='utf-8') as file:
                yield file.read()

    def insert(self, jsonobj):
        x28_id = jsonobj['id']
        title = jsonobj['title']
        html = jsonobj['htmlcontent']
        plaintext = jsonobj['plaincontent']
        url = jsonobj['url']
        cursor = self.conn_x28.cursor()
        sql = r"""INSERT INTO labeled_jobs(x28_id, html, plaintext, url, title) 
                          VALUES (%s,%s,%s,%s,%s)
                          ON CONFLICT(x28_id) DO UPDATE
                          SET html = excluded.html,
                              plaintext = excluded.plaintext,
                              url = excluded.url,
                              title = excluded.title
                              """
        cursor.execute(sql, (x28_id, html, plaintext, url, title))
        self.conn_x28.commit()

    def truncate_tables(self):
        logging.info('truncating target tables...')
        cursor = self.conn_x28.cursor()
        cursor.execute("""TRUNCATE labeled_jobs""")