import logging
import os
import sys

import pandas
from tqdm import tqdm

from src import db, preproc
from src.db import Database
from src.util import jobtitle_util

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

resource_dir = 'D:/code/ip7-python/resource'
known_jobs_tsv = os.path.join(resource_dir, 'known_jobs.tsv')


def truncate_target_tables():
    logging.info('truncating target tables')
    cursor = conn.cursor()
    cursor.execute("""TRUNCATE TABLE job_classes_variants""")
    cursor.execute("""TRUNCATE TABLE job_classes CASCADE""")
    conn.commit()


def import_job_names_from_file():
    logging.info('importing job names from {}'.format(known_jobs_tsv))
    df = pandas.read_csv(known_jobs_tsv, delimiter='\t', names=['job_name'])
    return df['job_name']


def create_job_variants(job_name):
    job_variants = jobtitle_util.create_variants(job_name)
    return job_variants


def add_job_class(job_name):
    job_name_stem = preproc.stem(job_name)
    cursor = conn.cursor()
    cursor.execute("""SELECT count(*) as cnt from job_classes where job_name = %s""", [job_name])
    if cursor.fetchone()['cnt'] == 0:
        cursor.execute("""INSERT INTO job_classes (job_name, job_name_stem) VALUES (%s, %s) RETURNING id""", (job_name, job_name_stem))
        conn.commit()
        return cursor.fetchone()[0]
    return -1


def add_job_variant(job_id, job_variant):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO job_classes_variants (job_class_id, job_name_variant) 
                      VALUES(%s, %s)""",
                   (job_id, job_variant))
    conn.commit()


conn = db.connect_to(Database.X28_PG)


def normalize_job_name(job_name):
    pass


if __name__ == '__main__':
    truncate_target_tables()
    job_names = import_job_names_from_file()
    for job_name in tqdm(job_names):
        job_name_normalized = normalize_job_name(job_name)
        job_id = add_job_class(job_name)
        if job_id > 0:
            job_variants = create_job_variants(job_name)
            for job_variant in job_variants:
                add_job_variant(job_id, job_variant)

conn.close()
