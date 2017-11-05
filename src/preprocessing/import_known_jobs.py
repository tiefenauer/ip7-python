import logging
import os
import re
import sys

import nltk
import pandas
import numpy as np
from tqdm import tqdm

from src import db
from src.db import Database
from src.util import jobtitle_util

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

resource_dir = 'D:/code/ip7-python/resource'
job_titles_tsv = os.path.join(resource_dir, 'job_titles.tsv')
known_jobs_tsv = os.path.join(resource_dir, 'known_jobs.tsv')


def import_job_names_from_file():
    logging.info('importing job names from {}'.format(job_titles_tsv))
    df = pandas.read_csv(job_titles_tsv, delimiter='\t', names=['job_name'])
    return df['job_name']


def import_job_name_from_fts():
    logging.info('importing job names from Full Text Search results')
    cursor = conn.cursor()
    sql = """SELECT a.title actual, p.job_name AS prediction
            FROM job_name_fts p
            LEFT OUTER JOIN labeled_jobs a ON a.id = p.job_id"""
    cursor.execute(sql)
    for row in cursor:
        job_name, origin = merge(row['actual'], row['prediction'])
        if job_name is not None:
            yield job_name, origin


def merge(actual, prediction):
    actual_n = jobtitle_util.to_male_form(actual)
    prediction_n = jobtitle_util.to_male_form(prediction)
    # full match
    if actual_n == prediction_n:
        return actual_n, 'predicted'
    # partial match / compound word
    words_actual = nltk.word_tokenize(re.escape(actual_n), language='german')
    words_prediction = nltk.word_tokenize(prediction_n, language='german')
    if prediction_n.lower() in actual_n.lower():
        if len(words_actual) == len(words_prediction):
            return actual_n, 'compound'
    # no match
    if len(words_actual) == 1:
        return actual_n, 'guessed'
    return None, None


def write_job_name_to_db(name, origin):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO known_jobs (job_name, origin) VALUES (%s, %s)""", (name, origin))
    conn.commit()


def truncate_target_table():
    logging.info('truncating target tables')
    cursor = conn.cursor()
    cursor.execute("""TRUNCATE TABLE known_jobs""")
    conn.commit()


def write_known_jobs_to_file():
    logging.info('writing entries of table known_jobs to file {}'.format(known_jobs_tsv))

    df = pandas.read_csv(known_jobs_tsv, delimiter='\t', names=['job_name'])
    logging.info('entries in {} before: {}'.format(known_jobs_tsv, df.shape[0]))

    sql = """SELECT DISTINCT job_name FROM known_jobs ORDER BY job_name ASC"""
    conn = db.connect_to(Database.X28_PG)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    all_jobs = pandas.DataFrame(np.array(data))

    logging.info('entries in {} after: {}'.format(known_jobs_tsv, all_jobs.shape[0]))
    all_jobs[0].to_csv(known_jobs_tsv, encoding='utf-8', index=False)


conn = db.connect_to(Database.X28_PG)

if __name__ == '__main__':
    truncate_target_table()
    new_jobs = set()
    known_jobs = import_job_names_from_file()
    for job_name in tqdm(known_jobs):
        write_job_name_to_db(job_name, 'job_titles.tsv')
        new_jobs.add(job_name.lower())
    fts_jobs = import_job_name_from_fts()
    for job_name, origin in tqdm(fts_jobs):
        if job_name.lower() not in new_jobs:
            write_job_name_to_db(job_name, 'fts ' + origin)
            new_jobs.add(job_name.lower())

    write_known_jobs_to_file()

conn.close()
