from src.importer.job_name_importer import JobNameImporter
from src.jobtitle.jobtitle_extractor import find_all_matches

_job_name_cached = JobNameImporter()


def find_best(tags, job_names=_job_name_cached):
    best_count = 0
    best_match = None
    for (count, name) in find_all(tags, job_names):
        if count > best_count:
            best_count = count
            best_match = name
    return best_match, best_count


def find_all(tags, job_names=_job_name_cached):
    for match in find_all_matches(tags, job_names):
        yield match
