from src.classifier import jobtitle_scorer as ranking
from src.classifier.classification_strategy import ClassificationStrategy
from src.importer.job_name_importer import JobNameImporter
from src.jobtitle import jobtitle_extractor as extractor


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

    def __init__(self):
        self.job_names = JobNameImporter()

    def classify(self, tags):
        best_match = None
        num_occurrence = 0
        best_score = 0
        for tag_features in (tag_features for tag_features in (self.extract_features(tag) for tag in tags) if
                             tag_features['matches']):
            score = ranking.calculate_score(tag_features)
            if score > best_score:
                best_score = score
                best_match, num_occurrence = next(iter(tag_features['matches']), (None, None))
        return best_match, num_occurrence, best_score

    def extract_features(self, tag, job_names=None):
        if job_names is None:
            job_names = self.job_names
        job_titles = extractor.extract_job_titles(str(tag), job_names)
        return {
            'tag': tag.name if tag.name else None,
            'matches': sorted(list(job_titles), key=lambda match: (match[1], match[0]),
                              reverse=True) if job_titles else []
        }

    def title(self):
        return self.TITLE

    def description(self):
        return self.DESCRIPTION

    def label(self):
        return 'feature-based'
