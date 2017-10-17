import logging
import operator
import sys

import pandas

from src.job_importer import process_stream
from src.train.util import create_contexts

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

_job_names = pandas.read_csv('../resource/tbfulljob_DE.csv', delimiter=';')
_job_names.columns = ['job_name']
_job_names = _job_names['job_name']


def match_with_whitelist(row, job_names=_job_names):
    dom_str = str(row['dom'])
    for job_name in (j for j in job_names if j in dom_str):
        yield {
            'job_id': row['id'],
            'job_name': job_name,
            'job_context': create_contexts(dom_str, job_name)
        }


def count_jobs_by_name(matches_for_jobs):
    matches_by_job_name = {}
    for matches_for_job in matches_for_jobs:
        for match in list(matches_for_job):
            id = match['job_id']
            name = match['job_name']
            context = ', '.join(match['job_context'])
            if not name in matches_by_job_name:
                matches_by_job_name[name] = 0
            matches_by_job_name[name] = matches_by_job_name[name] + 1
            # logging.info('Match: job_id={}, job_name={}, job_context={}'.format(id, name, context))
    return matches_by_job_name


def print_stats(job_counts):
    logging.info("Found the following jobs: ")
    num_classifications = sum(job_counts.values())
    job_counts_sorted = sorted(job_counts.items(), key=lambda k: k[1], reverse=True)
    pattern = "{:<30} {:<4}"
    print(pattern.format('Job Name', 'Count'))
    print('------------------------------------')
    for job_name, count in job_counts_sorted:
        print(pattern.format(job_name, count))
    print('------------------------------------')
    print(pattern.format('Total', num_classifications))
    print(pattern.format('Jobs per vacancy', num_classifications/(len(job_counts_sorted) or 1)))
    print('====================================')


if __name__ == '__main__':
    matches_for_jobs = (match_with_whitelist(row) for row in process_stream())
    matches_by_job_name = count_jobs_by_name(matches_for_jobs)
    print_stats(matches_by_job_name)
