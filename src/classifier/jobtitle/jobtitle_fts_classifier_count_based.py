from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.tag_classifier import TagClassifier
from src.dataimport.known_jobs import KnownJobs
from src.util.jobtitle_util import create_gender_variants, count_variant


def count_job_names(tags, job_names):
    html_text = "".join(str(tag) for tag in tags)
    for job_name in job_names:
        variants = create_gender_variants(job_name)
        if any(job_name_variant in html_text for job_name_variant in variants):
            count = 0
            for variant in variants:
                count += count_variant(variant, html_text)
            yield (count, job_name)


class CountBasedJobtitleFtsClassifier(TagClassifier, JobtitleClassifier):
    """Predict a jobtitle by performing a full text search (FTS) on the processed data. The processed data is searched
    for occurrences of known job names, including variants (such as male/female form, hyphenated forms etc...).
    The job name with the highest occurrence is used as extracted job title."""

    def __init__(self, args):
        super(CountBasedJobtitleFtsClassifier, self).__init__(args)
        self.known_jobs = KnownJobs()

    def classify(self, relevant_tags):
        best_count = 0
        best_match = None
        for (count, name) in count_job_names(relevant_tags, self.known_jobs):
            if count > best_count:
                best_count = count
                best_match = name
        return best_match

    def title(self):
        return 'Jobtitle Classifier: FTS (count-based)'

    def label(self):
        return 'jobtitle-fts-count'
