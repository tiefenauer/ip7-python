import logging

import sys
from tqdm import tqdm

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def process_stream(callback):
    conn = db.connect_to(Database.FETCHFLOW)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT count(*) AS num_total FROM labeled_text")
    num_total = cursor.fetchone()['num_total']
    logging.info('processing {} rows'.format(num_total))

    batchsize = 1000
    for i in tqdm(range(0, num_total, batchsize), unit_scale=batchsize, unit=' rows'):
        cursor.execute("SELECT id, title, contentbytes AS dom FROM labeled_text WHERE has_job_title = 0 LIMIT %s OFFSET %s",
                       (batchsize, batchsize))
        for row in cursor:
            yield callback(row)
