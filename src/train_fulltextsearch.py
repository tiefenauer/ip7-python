import logging
import sys

from src.importer import FetchflowImporter, JobNameImporter
from src.stats import print_stats
from src.train.util import create_contexts

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def process_row(row):
    return find_matches_in_dom(str(row['dom']))


def find_matches_in_dom(dom):
    for job_name in (j for j in job_names if j in dom):
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
    job_names = JobNameImporter()
    with FetchflowImporter() as fetchflow:
        for job_matches in (process_row(row) for row in fetchflow):
            stats = count_jobs_by_name(job_matches)
    print_stats(stats)
