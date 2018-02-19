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
from pony.orm import commit
from tqdm import tqdm

from src.database.entities_pg import Classification_Results, Job_Class
from src.util import jobtitle_util
from src.util.globals import RESOURCE_DIR
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

job_titles_tsv = os.path.join(RESOURCE_DIR, 'job_titles.tsv')
known_jobs_dirty = os.path.join(RESOURCE_DIR, 'known_jobs_dirty.tsv')

slashed_jobname_pattern = re.compile('(?<=[a-z])\/(?=[A-Z])')
trailing_special_chars_pattern = re.compile(r'[\s\/\-_]+$')
leading_special_chars_pattern = re.compile(r'^[\s\/\-_]')


def import_job_names_from_file():
    log.info('importing job names from {}'.format(job_titles_tsv))
    df = pandas.read_csv(job_titles_tsv, delimiter='\t', names=['job_name'])
    return df['job_name']


def import_job_name_from_fts():
    log.info('importing job names from Full Text Search results')
    for result in Classification_Results.select(lambda c: c.clf_method == 'jobtitle-fts'):
        actual = result.job.title
        predicted = result.job_name
        for job_name in merge(actual, predicted):
            yield job_name


def merge(actual, prediction):
    merged_job_names = set()
    # split on slashes but not if slash denotss a male/female form
    actual_job_names = re.split(slashed_jobname_pattern, actual)
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
    str = re.sub(trailing_special_chars_pattern, '', str)
    # remove leading special chars
    str = re.sub(leading_special_chars_pattern, '', str)
    return str


def write_job_name_to_db(job_name):
    Job_Class(job_name=job_name)
    commit()


def truncate_target_table():
    log.info('truncating target tables')
    Job_Class.select().delete(bulk=True)
    commit()


def write_known_jobs_to_file():
    log.info('writing entries of table known_jobs to file {}'.format(known_jobs_dirty))

    df = pandas.read_csv(known_jobs_dirty, delimiter='\t', names=['job_name'])
    log.info('entries in {} before: {}'.format(known_jobs_dirty, df.shape[0]))

    job_names = list(row.job_name for row in Job_Class.select().order_by(Job_Class.job_name))
    all_jobs = pandas.DataFrame(np.array(job_names))

    log.info('entries in {} after: {}'.format(known_jobs_dirty, all_jobs.shape[0]))
    all_jobs[0].to_csv(known_jobs_dirty, encoding='utf-8', index=False)


if __name__ == '__main__':
    truncate_target_table()
    new_jobs = set()

    known_jobs = import_job_names_from_file()
    for job_name in tqdm(known_jobs):
        write_job_name_to_db(job_name)
        new_jobs.add(job_name.lower())

    fts_jobs = import_job_name_from_fts()
    for job_name in tqdm(fts_jobs):
        if job_name.lower() not in new_jobs:
            write_job_name_to_db(job_name)
            new_jobs.add(job_name.lower())

    write_known_jobs_to_file()
