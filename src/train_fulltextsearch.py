import argparse
import itertools
import logging
import sys

from src.preproc import preprocess
from src.importer.fetchflow_importer import FetchflowImporter
from src.importer.job_name_importer import JobNameImporter
from src.jobtitle.jobtitle_extractor import find_all_matches
from src.stats import print_stats

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="""
Extracts job titles by performing a full text search (brute force). The DOM is scanned for occurrences of known job 
names from a whitelist stored in ./resources/job_titles.tsv.
The vacancy is classified as the job name with the highest number of occurrences (or none, if the DOM does not contain
any of the job names from the whitelist).
The extraction considers deviant writings of job names such as female forms. This means if the whitelist contains a
job name in the male form (e.g. 'Schreiner', 'Coiffeur' or 'Kaufmann') the respective female forms are also found
('Schreinerin', 'Coiffeuse' or 'Kauffrau').
The classified job name includes extended information where possible. If a DOM contains for example the string 
'Software Engineer (m/w)', whereas 'Software Engineer' would be the matching job name from the whitelist, the full
string 'Software Engineer (m/w)' will be used as extracted job name, not just the one from the whitelist.
""")
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-c', '--save_contexts', action='store_true',
                    help='enable simple processing. Simple processing means '
                         'only the job name with the highest occurrence will be '
                         'stored together with the number of occurrences. No '
                         'context information or alternatives will be stored!')
args = parser.parse_args()

_job_name_cached = JobNameImporter()


def find_all(text, job_names=_job_name_cached):
    for match in find_all_matches(text, job_names):
        yield match


def find_best(text, job_names=_job_name_cached):
    best_match = None
    best_count = 0
    grouped = itertools.groupby(find_all(text, job_names), key=lambda m: m.group())
    for (k, g) in grouped:
        count = len(list(g))
        if count > best_count:
            best_count = count
            best_match = k
    return best_match, best_count


def update_stats(matches, stats):
    for match in matches:
        name = match['job_name']
        if not name in stats:
            stats[name] = 0
        stats[name] += 1


if __name__ == '__main__':
    stats = {}
    with FetchflowImporter() as fetchflow:
        if args.truncate:
            fetchflow.truncate_results()
        for row in (row for row in fetchflow if row['dom']):
            text = preprocess(row['dom'])
            (job_title, job_count) = find_best(text)
            if job_title is not None:
                fetchflow.update_job_with_title(row, job_title, job_count)
    print_stats(stats)
