# collects all known jobs by reading from job_titles.csv and evaluating the results from full text search (FTS)
# Results are written to known_jobs_dirty.tsv
# Because the X28-Target classes are not really clean (not real job names, duplicates, spelling errors, overlapping
# classes), the results in known_jobs_dirty.tsv must be postprocessed by hand!
import logging
import os
import re

import nltk
import numpy as np
import pandas
from tqdm import tqdm

from src import db
from src.db import Database
from src.util import jobtitle_util
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

resource_dir = 'D:/code/ip7-python/resource'
job_titles_tsv = os.path.join(resource_dir, 'job_titles.tsv')
known_jobs_dirty = os.path.join(resource_dir, 'known_jobs_dirty.tsv')


def import_job_names_from_file():
    log.info('importing job names from {}'.format(job_titles_tsv))
    df = pandas.read_csv(job_titles_tsv, delimiter='\t', names=['job_name'])
    return df['job_name']


def import_job_name_from_fts():
    log.info('importing job names from Full Text Search results')
    cursor = conn.cursor()
    sql = """SELECT a.title actual, p.job_name AS prediction
            FROM classification_results p
            LEFT OUTER JOIN x28_data a ON a.id = p.job_id
            WHERE clf_method=jobtitleitle'
            """
    cursor.execute(sql)
    for row in cursor:
        for job_name in merge(row['actual'], row['prediction']):
            yield job_name


def merge(actual, prediction):
    merged_job_names = set()
    # split on slashes but not if slash denotss a male/female form
    actual_job_names = re.split('(?<=[a-z])\/(?=[A-Z])', actual)
    for actual_job_name in actual_job_names:
        actual_n = jobtitle_util.to_male_form(actual_job_name)
        actual_n = trim_and_remove_special_chars(actual_n)
        prediction_n = jobtitle_util.to_male_form(prediction)
        prediction_n = trim_and_remove_special_chars(prediction_n)
        # full match
        if actual_n == prediction_n:
            merged_job_names.add(actual_n)
            continue
        # partial match / compound word
        words_actual = nltk.word_tokenize(re.escape(actual_n), language='german')
        words_prediction = nltk.word_tokenize(prediction_n, language='german')
        if prediction_n.lower() in actual_n.lower():
            if len(words_actual) == len(words_prediction):
                merged_job_names.add(actual_n)
        # no match
        if len(words_actual) == 1:
            merged_job_names.add(actual_n)
    return merged_job_names


def trim_and_remove_special_chars(str):
    # remove trailing special chars
    str = re.sub(r'[\s\/\-_]+$', '', str)
    # remove leading special chars
    str = re.sub(r'^[\s\/\-_]', '', str)
    return str


def write_job_name_to_db(name, origin):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO known_jobs (job_name, origin) VALUES (%s, %s)""", (name, origin))
    conn.commit()


def truncate_target_table():
    log.info('truncating target tables')
    cursor = conn.cursor()
    cursor.execute("""TRUNCATE TABLE known_jobs""")
    conn.commit()


def write_known_jobs_to_file():
    log.info('writing entries of table known_jobs to file {}'.format(known_jobs_dirty))

    df = pandas.read_csv(known_jobs_dirty, delimiter='\t', names=['job_name'])
    log.info('entries in {} before: {}'.format(known_jobs_dirty, df.shape[0]))

    sql = """SELECT DISTINCT job_name FROM known_jobs ORDER BY job_name ASC"""
    conn = db.connect_to(Database.X28_PG)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    all_jobs = pandas.DataFrame(np.array(data))

    log.info('entries in {} after: {}'.format(known_jobs_dirty, all_jobs.shape[0]))
    all_jobs[0].to_csv(known_jobs_dirty, encoding='utf-8', index=False)


conn = db.connect_to(Database.X28_PG)

if __name__ == '__main__':
    truncate_target_table()
    new_jobs = set()
    known_jobs = import_job_names_from_file()
    for job_name in tqdm(known_jobs):
        write_job_name_to_db(job_name, 'job_titles.tsv')
        new_jobs.add(job_name.lower())
    fts_jobs = import_job_name_from_fts()
    for job_name in tqdm(fts_jobs):
        if job_name.lower() not in new_jobs:
            write_job_name_to_db(job_name, 'jobtitle')
            new_jobs.add(job_name.lower())

    write_known_jobs_to_file()

conn.close()
