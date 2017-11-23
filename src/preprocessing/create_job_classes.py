# Fills tables job_class and job_class_variant on DB by reading from known_jobs.tsv
# Each row in known_jobs.tsv will be a class in job_class
# For each class the different writing and gender variants are created
# Each created variant will be a row in job_class_variant
import logging
import os
import re

import pandas
from tqdm import tqdm

from src import db, preproc
from src.db import Database
from src.util import jobtitle_util
from src.util.boot_util import log_setup

log_setup()
log = logging.getLogger(__name__)

resource_dir = 'D:/code/ip7-python/resource'
known_jobs_tsv = os.path.join(resource_dir, 'known_jobs.tsv')


def truncate_target_tables():
    log.info('truncating target tables')
    cursor = conn.cursor()
    cursor.execute("""TRUNCATE TABLE job_class_variant""")
    cursor.execute("""TRUNCATE TABLE job_class CASCADE""")
    conn.commit()


def import_job_names_from_file():
    log.info('importing job names from {}'.format(known_jobs_tsv))
    df = pandas.read_csv(known_jobs_tsv, delimiter='\t', names=['job_name'])
    return df['job_name']


def write_job_classes_from_db_to_file():
    log.info('writing classes back to file: {}'.format(known_jobs_tsv))
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT job_namee AS job_name FROM job_class ORDER BY job_name ASC""")
    with open(known_jobs_tsv, mode='w+', encoding='utf-8') as file:
        file.truncate()
        for row in cursor:
            file.write(row['job_name'] + '\n')


def create_gender_variants(job_name):
    job_variants = jobtitle_util.create_gender_variants(job_name)
    return job_variants


def create_write_variants(job_name):
    write_variants = set()
    write_variants.add(job_name)
    if is_hyphenated(job_name):
        job_name_parts = re.findall('([a-zA-Z]+)', job_name)
        part1 = job_name_parts[0]
        part2 = job_name_parts[1]
        job_concatenated = create_job_name_concatenated(part1, part2.lower())
        job_spaced = create_job_name_spaced(part1, part2)
        write_variants.add(job_concatenated)
        write_variants.add(job_spaced)
    else:
        for known_job in known_jobs:
            if known_job.lower() in job_name:
                part1 = job_name.split(known_job.lower())[0].strip()
                job_concatenated = create_job_name_concatenated(part1, known_job.lower())
                job_spaced = create_job_name_spaced(part1, known_job)
                job_hyphenated = create_job_name_hyphenated(part1, known_job)
                write_variants.add(job_concatenated)
                write_variants.add(job_spaced)
                write_variants.add(job_hyphenated)

    return write_variants


def create_job_name_spaced(job_name_1, job_name_2):
    return job_name_1 + ' ' + job_name_2


def create_job_name_concatenated(job_name_1, job_name_2):
    return job_name_1 + job_name_2


def create_job_name_hyphenated(job_name_1, job_name_2):
    return job_name_1 + '-' + job_name_2


hyphenated_pattern = re.compile('(?=\S*[-])([a-zA-Z-]+)')


def is_hyphenated(job_name):
    return hyphenated_pattern.match(job_name)


def add_job_class(job_class):
    job_name_stemmed = preproc.stem(job_class)
    cursor = conn.cursor()
    cursor.execute("""SELECT count(*) AS cnt FROM job_class WHERE job_name = %s""", [job_class])
    if cursor.fetchone()['cnt'] == 0:
        cursor.execute("""INSERT INTO job_class (job_name, job_name_stem) VALUES (%s, %s) RETURNING id""",
                       (job_class, job_name_stemmed))
        conn.commit()
        return cursor.fetchone()[0]
    return -1


def add_job_variant(job_id, job_variant):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO job_class_variant (job_class_id, job_name_variant) 
                      VALUES(%s, %s)""",
                   (job_id, job_variant))
    conn.commit()


known_jobs = import_job_names_from_file()

conn = db.connect_to(Database.X28_PG)

if __name__ == '__main__':
    truncate_target_tables()

    for job_name in tqdm(known_jobs):
        job_id = add_job_class(job_name)
        variants = set()
        write_variants = create_write_variants(job_name)
        variants.update(write_variants)
        for write_variant in write_variants:
            gender_variants = create_gender_variants(write_variant)
            variants.update(gender_variants)

        for job_variant in variants:
            if job_id > 0:
                add_job_variant(job_id, job_variant)

    write_job_classes_from_db_to_file()

conn.close()
