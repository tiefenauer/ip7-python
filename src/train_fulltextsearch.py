import logging
import sys

from src.importer import FetchflowImporter, JobNameImporter
from src.stats import print_stats
from src.train.util import create_contexts

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def process_row(row):
    return (match for match in find_matches(str(row['dom'])) if match is not None)


def find_matches(dom):
    for job_name in (job_name for job_name in job_names if job_name in dom):
        yield {
            'job_name': job_name,
            'job_contexts': create_contexts(dom, job_name)
        }


def update_stats(matches, stats):
    for match in matches:
        name = match['job_name']
        if not name in stats:
            stats[name] = 0
        stats[name] += 1


if __name__ == '__main__':
    job_names = JobNameImporter()
    stats = {}
    with FetchflowImporter() as fetchflow:
        for row, matches in ((row, process_row(row)) for row in fetchflow):
            fetchflow.update_job(row, matches)
            update_stats(matches, stats)
    print_stats(stats)
