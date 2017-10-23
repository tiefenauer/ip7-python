import logging
import sys

from src.extractor.jobtitle_extractor import find_matches
from src.importer import FetchflowImporter, JobNameImporter
from src.stats import print_stats

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def process_row(row, job_names=JobNameImporter()):
    for match in find_matches(str(row['dom']), job_names):
        yield match


def update_stats(matches, stats):
    for match in matches:
        name = match['job_name']
        if not name in stats:
            stats[name] = 0
        stats[name] += 1


if __name__ == '__main__':
    stats = {}
    with FetchflowImporter() as fetchflow:
        for row, matches in ((row, process_row(row)) for row in fetchflow):
            fetchflow.update_job(row, matches)
            update_stats(matches, stats)
    print_stats(stats)
