from src.dataimport.known_jobs_tsv_importer import KnownJobsImporter
from src.classifier.jobtitle.jobtitle_fts_classifier import JobtitleFtsClassifier
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


class CountBasedJobtitleFtsClassifier(JobtitleFtsClassifier):
    def __init__(self, args, preprocessor):
        super(CountBasedJobtitleFtsClassifier, self).__init__(args, preprocessor)
        self.job_names = KnownJobsImporter()

    def extract(self, tags):
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
        return 'Jobtitle Extractor: FTS (count-based)'

    def description(self):
        return """Extract a jobtitle by performing a full text search (FTS) on the DOM. The text of the DOM is searched
        for occurrences of known job names, including variants (such as male/female form, hyphenated forms etc...).
        The job name with the highest occurrence is used as extracted job title."""

    def label(self):
        return 'jobtitle-jobtitle-count'
