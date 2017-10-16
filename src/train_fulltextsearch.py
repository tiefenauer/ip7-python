import collections
import logging
import re
import sys

import pandas

from src.job_importer import process_stream

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

_job_names = pandas.read_csv('../resource/tbfulljob_DE.csv', delimiter=';')
_job_names.columns = ['job_name']
_job_names = _job_names['job_name']


def match_with_whitelist(row, job_names=_job_names):
    dom_str = str(row['dom'])
    for job_name in job_names:
        indices = find_str1_in_str2(job_name, dom_str)

        if indices:
            yield {
                'job_id': row['id'],
                'job_name': job_name,
                'job_context': create_contexts(indices, dom_str, job_name)
            }


def find_str1_in_str2(str1, str2):
    """finds indices of occurences of str1 in str2"""
    return [match.start() for match in re.finditer(re.escape(str1), str2)]


def create_contexts(indices, text, word):
    contexts = list()
    for ix in indices:
        contexts.append('...' + text[ix - 10:ix + len(word) + 10] + '...')
    return contexts


def flatten(it):
    for x in it:
        if (isinstance(x, collections.Iterable) and
                not isinstance(x, str)):
            yield from flatten(x)
        else:
            yield x


if __name__ == '__main__':
    matches_for_jobs = process_stream(match_with_whitelist)
    for matches_for_job in matches_for_jobs:
        for match in list(matches_for_job):
            id = match['job_id']
            name = match['job_name']
            context = ', '.join(match['job_context'])
            logging.info('Match: job_id={}, job_name={}, job_context={}'.format(id, name, context))
    logging.info("done!")
