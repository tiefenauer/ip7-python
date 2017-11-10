from src.classifier.classification_strategy import ClassificationStrategy
from src.classifier.fts_classifier import FullTextSearchClassifier
from src.importer.known_jobs_tsv_importer import KnownJobsImporter
from src.util.jobtitle_util import create_gender_variants, count_variant


def find_all_matches(tags, job_names):
    html_text = "".join(str(tag) for tag in tags)
    for job_name in job_names:
        variants = create_gender_variants(job_name)
        if any(job_name_variant in html_text for job_name_variant in variants):
            count = 0
            for variant in variants:
                count += count_variant(variant, html_text)
            yield (count, job_name)


class CountBasedJobTitleClassification(FullTextSearchClassifier):
    TITLE = """Count-based classification"""
    DESCRIPTION = """Classify a vacancy based on the number of occurrences of a certain word. The words are jobs
    taken from a whitelist of known job names. The occurrence of each job name is counted and the vacancy is then
    classified as the job name with the highest occurrence."""

    def __init__(self, model_file=None):
        super(CountBasedJobTitleClassification, self).__init__(model_file)
        self.job_names = KnownJobsImporter()

    def classify(self, tags):
        best_count = 0
        best_match = None
        for (count, name) in self.find_all(tags, self.job_names):
            if count > best_count:
                best_count = count
                best_match = name
        return best_match, best_count, 1

    def find_all(self, tags, job_names=None):
        if job_names is None:
            job_names = self.job_names
        for match in find_all_matches(tags, job_names):
            yield match

    def title(self):
        return self.TITLE

    def description(self):
        return self.DESCRIPTION

    def label(self):
        return 'count-based'
