# Fills tables job_class and job_class_variant on DB by reading from known_jobs.tsv
# Each row in known_jobs.tsv will be a class in job_class
# For each class the different writing and gender variants are created
# Each created variant will be a row in job_class_variant
import logging
import re

from pony.orm import commit
from tqdm import tqdm

from src import preproc
from src.database.entities_pg import Job_Class, Job_Class_Variant
from src.dataimport.known_jobs import KnownJobs
from src.util import jobtitle_util
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

resource_dir = 'D:/code/ip7-python/resource'
known_jobs_tsv = os.path.join(resource_dir, 'known_jobs.tsv')

job_name_part_pattern = re.compile('([a-zA-Z]+)')


def truncate_target_tables():
    log.info('truncating target tables')
    Job_Class.select().delete(bulk=True)
    Job_Class_Variant().select().delete(bulk=True)
    commit()


def write_job_classes_from_db_to_file():
    log.info('writing classes back to file: {}'.format(known_jobs_tsv))
    with open(known_jobs_tsv, mode='w+', encoding='utf-8') as file:
        file.truncate()
        for row in Job_Class.select().order_by(Job_Class.job_name):
            file.write(row.job_name + '\n')


def create_write_variants(job_name):
    write_variants = set()
    write_variants.add(job_name)
    if jobtitle_util.is_hyphenated(job_name):
        job_name_parts = re.findall(job_name_part_pattern, job_name)
        part1 = job_name_parts[0]
        part2 = job_name_parts[1]
        job_concatenated = jobtitle_util.to_concatenated_form(part1, part2)
        job_spaced = jobtitle_util.to_spaced_form(part1, part2)
        write_variants.add(job_concatenated)
        write_variants.add(job_spaced)
    else:
        for known_job in known_jobs:
            if known_job.lower() in job_name:
                part1 = job_name.split(known_job.lower())[0].strip()
                job_concatenated = jobtitle_util.to_concatenated_form(part1, known_job)
                job_spaced = jobtitle_util.to_spaced_form(part1, known_job)
                job_hyphenated = jobtitle_util.to_hyphenated_form(part1, known_job)
                write_variants.add(job_concatenated)
                write_variants.add(job_spaced)
                write_variants.add(job_hyphenated)

    return write_variants


def add_job_class(job_name):
    job_name_stemmed = preproc.stem(job_name)
    existing_num = Job_Class.select(lambda j: j.job_name == job_name).count()
    if existing_num == 0:
        job_class = Job_Class(job_name=job_name, job_name_stemmed=job_name_stemmed)
        commit()
        return job_class
    return None


def add_job_variant(job_class, job_name_variant):
    job_class_variant = Job_Class_Variant(job_class=job_class, job_name_variant=job_name_variant)
    commit()
    return job_class_variant


if __name__ == '__main__':
    truncate_target_tables()

    known_jobs = KnownJobs()
    for job_name in tqdm(known_jobs):
        job_class = add_job_class(job_name)
        variants = set()
        write_variants = create_write_variants(job_name)
        variants.update(write_variants)
        for write_variant in write_variants:
            gender_variants = jobtitle_util.create_gender_variants(write_variant)
            variants.update(gender_variants)

        if job_class:
            for job_variant in variants:
                add_job_variant(job_class, job_variant)

    write_job_classes_from_db_to_file()
