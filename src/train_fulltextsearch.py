import logging
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


if __name__ == '__main__':
    matches_for_jobs = process_stream(match_with_whitelist)
    matches_by_job_name = {}
    for matches_for_job in matches_for_jobs:
        for match in list(matches_for_job):
            id = match['job_id']
            name = match['job_name']
            context = ', '.join(match['job_context'])
            if not name in matches_by_job_name:
                matches_by_job_name[name] = 0
            matches_by_job_name[name] = matches_by_job_name[name]+1
            # logging.info('Match: job_id={}, job_name={}, job_context={}'.format(id, name, context))
    logging.info("Found the following jobs: " + matches_by_job_name)
