from src.classifier.classification_strategy import ClassificationStrategy
from src.importer.job_name_importer import JobNameImporter
from src.jobtitle import jobtitle_extractor as extractor
from src.jobtitle.jobtitle_matcher import count_variant, create_variants

job_names = JobNameImporter()
tag_weight = {
    'h1': 0.6,
    'h2': 0.3,
    'h3': 0.1,
    'default': 0.1
}


def extract_features(tag, job_names=job_names):
    job_titles = extract_job_titles(str(tag), job_names)
    return {
        'tag': tag.name if tag.name else None,
        'matches': sorted(list(job_titles), key=lambda match: (match[1], match[0]),
                          reverse=True) if job_titles else []
    }


def extract_job_titles(string, job_names):
    for job_name in job_names:
        variants = create_variants(job_name)
        if any(job_name_variant in string for job_name_variant in variants):
            count = 0
            for variant in variants:
                count += count_variant(variant, string)
            yield (job_name, count)


class FeatureBasedJobTitleClassification(ClassificationStrategy):
    TITLE = """"Feature based classification"""
    DESCRIPTION = """Feature-Based classification: classifies a vacancy according to the features of the
        individual tags. Each tag is analyzed in isolation. Only tags which contain known job names (from a whitelist)
        or variants of them are considered. A tag can contain several job names or variants.
        For each tag the relevant features are extracted. Relevant features can be:
        - the name of the tag
        - the number of occurrences for the individual matches
        Classification is then made by calculating a score based on the extracted features. The vacancy is classified
        as the job name with the highest occurrence from the tag with the highest score."""

    def __init__(self, job_names=job_names):
        self.job_names = job_names

    def classify(self, tags):
        best_match = None
        num_occurrence = 0
        best_score = 0
        for tag_features in (tag_features for tag_features in
                             (extract_features(tag) for tag in tags)
                             if tag_features['matches']):
            score = self.calculate_score(tag_features)
            if score > best_score:
                best_score = score
                best_match, num_occurrence = next(iter(tag_features['matches']), (None, None))
        return best_match, num_occurrence, best_score

    def calculate_score(self, features):
        rank = 0
        key = features['tag'] if features['tag'] in tag_weight else 'default'
        rank += tag_weight[key]
        # todo: add more feature values here if available
        return self.normalize(rank)

    def normalize(self, score):
        if score < 1:
            return score
        return 1 / score

    def title(self):
        return self.TITLE

    def description(self):
        return self.DESCRIPTION

    def label(self):
        return 'feature-based'
