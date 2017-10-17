import logging
import sys

from tqdm import tqdm

from src import db
from src.db import Database
import pandas as pd

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def process_stream():
    conn = db.connect_to(Database.FETCHFLOW)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT count(*) AS num_total FROM labeled_text")
    num_total = cursor.fetchone()['num_total']
    logging.info('processing {} rows'.format(num_total))

    chunksize = 1000
    sql = "SELECT id, title, contentbytes AS dom FROM labeled_text WHERE has_job_title = 0"
    chunks = pd.read_sql(sql=sql, con=conn, chunksize=chunksize)
    for chunk in tqdm(chunks, total=int(num_total/chunksize), unit_scale=chunksize, unit=' rows'):
        for row in chunk.to_dict('records'):
            yield row
