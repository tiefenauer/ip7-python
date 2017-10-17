import logging
import sys

from tqdm import tqdm

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def import_all():
    conn = db.connect_to(Database.FETCHFLOW)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT count(*) AS num_total FROM labeled_text")
    num_total = cursor.fetchone()['num_total']
    logging.info('processing {} rows'.format(num_total))

    cursor.execute("SELECT id, title, contentbytes AS dom FROM labeled_text WHERE has_job_title = 0")
    for row in tqdm(cursor, total=num_total, unit=' rows'):
        yield row
