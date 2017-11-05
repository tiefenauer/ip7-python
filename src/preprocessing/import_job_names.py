import os
import re

import nltk
import pandas

from src import db
from src.db import Database
from src.util import jobtitle_util

resource_dir = 'D:/code/ip7-python/resource'


def import_job_names_from_file():
    filename = os.path.join(resource_dir, 'job_titles.tsv')
    df = pandas.read_csv(filename, delimiter='\t', names=['job_name'])
    return df['job_name']


def import_job_name_from_fts():
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT a.title actual, p.job_name AS prediction
            FROM job_name_fts p
            LEFT OUTER JOIN labeled_jobs a ON a.id = p.job_id"""
    cursor.execute(sql)
    for row in cursor:
        job_name = merge(row['actual'], row['prediction'])
        yield job_name


def merge(actual, prediction):
    actual_n = jobtitle_util.to_male_form(actual)
    prediction_n = jobtitle_util.to_male_form(prediction)
    # full match
    if actual_n == prediction_n:
        return actual_n
    # partial match / compound word
    words_actual = nltk.word_tokenize(re.escape(actual_n), language='german')
    words_prediction = nltk.word_tokenize(prediction_n, language='german')
    if prediction_n.lower() in actual_n.lower():
        if len(words_actual) == len(words_prediction):
            return actual
    # no match
    if len(words_actual) == 1:
        return actual_n
    return None


def write_job_names_to_db(job_names):
    pass


conn = db.connect_to(Database.FETCHFLOW_PG)
if __name__ == '__main__':
    job_names_from_file = import_job_names_from_file()
    job_names_from_fts = import_job_name_from_fts()
    write_job_names_to_db(job_names)

conn.close()
