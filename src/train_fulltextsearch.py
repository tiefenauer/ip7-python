import collections
import logging
import re
import sys

import pandas

from src.job_importer import process_stream

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

_job_names = pandas.read_csv('../resource/tbfulljob_DE.csv', delimiter=';')
_job_names.columns = ['job_name']


def match_with_whitelist(row, job_names=_job_names):
    dom_str = str(row['dom'])
    for job_name in job_names:
        indices = find_string_occurences(job_name, dom_str)

        if indices:
            logging.info('Found one!')
            yield {
                'job_name': job_name,
                'job_context': create_contexts(indices, dom_str, job_name)
            }


def find_string_occurences(str1, str2):
    """finds indices of occurences of str1 in str2"""
    return [match.start() for match in re.finditer(str1, str2)]


def flatten(it):
    for x in it:
        if (isinstance(x, collections.Iterable) and
                not isinstance(x, str)):
            yield from flatten(x)
        else:
            yield x


if __name__ == '__main__':
    result = process_stream(match_with_whitelist)
    result = flatten(result)
    for matches in result:
        matches_set = set(matches)
        logging.info('Match: ' + matches)
    logging.info("done!")


def create_contexts(indices, text, word):
    contexts = list()
    for ix in indices:
        contexts.append('...' + text[ix-10:ix+len(word)+10] + '...')
    return contexts