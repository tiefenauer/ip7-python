import logging
import sys

import pandas

from src.job_importer import import_all
from src.stats import print_stats
from src.train.util import create_contexts

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

_job_names = pandas.read_csv('../resource/tbfulljob_DE.csv', delimiter=';')
_job_names.columns = ['job_name']
_job_names = _job_names['job_name']


def process_row(row):
    return find_matches_in_dom(str(row['dom']))


def find_matches_in_dom(dom):
    for job_name in (j for j in _job_names if j in dom):
        yield {
            'job_name': job_name,
            'job_context': create_contexts(dom, job_name)
        }


def count_jobs_by_name(matches, stat={}):
    for match in matches:
        name = match['job_name']
        if not name in stat:
            stat[name] = 0
        stat[name] += 1
    return stat


if __name__ == '__main__':
    for job_matches in (process_row(row) for row in import_all()):
        stats = count_jobs_by_name(job_matches)
    print_stats(stats)
