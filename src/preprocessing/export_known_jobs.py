import logging
import numpy as np
import os

import pandas
import sys

from src import db
from src.db import Database

resource_dir = 'D:/code/ip7-python/resource'
filename = os.path.join(resource_dir, 'known_jobs.tsv')
logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    df = pandas.read_csv(filename, delimiter='\t', names=['job_name'])
    logging.info('entries in {} before: {}'.format(filename, df.shape[0]))
    sql = """SELECT DISTINCT job_name FROM known_jobs ORDER BY job_name ASC"""
    conn = db.connect_to(Database.X28_PG)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    all_jobs = pandas.DataFrame(np.array(data))
    logging.info('entries in {} after: {}'.format(filename, all_jobs.shape[0]))

    logging.info('writing all entries to {}'.format(filename))
    all_jobs[0].to_csv(filename, encoding='utf-8', index=False)
