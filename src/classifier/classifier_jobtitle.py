from src.classifier import jobtitle_scorer as ranking
from src.importer.job_name_importer import JobNameImporter
from src.jobtitle import jobtitle_extractor as extractor

_job_names_cached = JobNameImporter()


def classify(tags):
    best_match = None
    num_occurrence = 0
    best_score = 0
    for tag_features in (tag_features for tag_features in (extract_features(tag) for tag in tags) if tag_features['matches']):
        score = ranking.calculate_score(tag_features)
        if score > best_score:
            best_score = score
            best_match, num_occurrence = next(iter(tag_features['matches']), (None, None))
    return best_match, num_occurrence, best_score


def find_best(tags, job_names=_job_names_cached):
    best_count = 0
    best_match = None
    for (count, name) in find_all(tags, job_names):
        if count > best_count:
            best_count = count
            best_match = name
    return best_match, best_count


def find_all(tags, job_names=_job_names_cached):
    for match in extractor.find_all_matches(tags, job_names):
        yield match


def extract_features(tag):
    job_titles = extractor.extract_job_titles(str(tag), _job_names_cached)
    return {
        'tag': tag.name if tag.name else None,
        'matches': sorted(list(job_titles), key=lambda match: (match[1], match[0]), reverse=True) if job_titles else []
    }
