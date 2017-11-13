import logging
import sys

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class PreprocessedData(object):
    def __enter__(self):
        self.db_fetchflow = db.connect_to(Database.FETCHFLOW_PG)
        cursor = self.db_fetchflow.cursor(dictionary=True)
        cursor.execute("SELECT count(*) AS num_rows FROM labeled_text")
        self.num_rows = cursor.fetchone()['num_rows']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_fetchflow.close()

    def __iter__(self):
        cursor = self.db_fetchflow.cursor(dictionary=True)
        cursor.execute("SELECT id, fetchflow_id, content FROM labeled_text")
        for row in cursor:
            yield row

    def insert(self, fetchflow_id, data):
        content = r"".join(str(tag) for tag in data)
        cursor = self.db_fetchflow.cursor()
        cursor.execute("""INSERT INTO labeled_text(fetchflow_id, content) VALUES(%s, %s)""", (fetchflow_id, content))
        self.db_fetchflow.commit()
