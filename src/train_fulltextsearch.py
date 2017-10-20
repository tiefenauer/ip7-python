import logging
import sys

from src.importer import FetchflowImporter, JobNameImporter
from src.stats import print_stats
from src.train.util import create_contexts

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def _by_number_of_contexts(match): return len(match['job_contexts'])


def process_row(row):
    sorted_list = sorted(list(find_matches(str(row['dom']))), key=_by_number_of_contexts, reverse=True)
    return next(iter(sorted_list), None)


def find_matches(dom):
    for job_name in (j for j in job_names if j in dom):
        yield {
            'job_name': job_name,
            'job_contexts': create_contexts(dom, job_name)
        }


def update_stats(match, stats):
    name = match['job_name'] if match is not None else 'unclassified'
    if not name in stats:
        stats[name] = 0
    stats[name] += 1


if __name__ == '__main__':
    job_names = JobNameImporter()
    stats = {}
    with FetchflowImporter() as fetchflow:
        for row in fetchflow:
            match = process_row(row)
            fetchflow.update_job(row, match)
            update_stats(match, stats)
    print_stats(stats)
