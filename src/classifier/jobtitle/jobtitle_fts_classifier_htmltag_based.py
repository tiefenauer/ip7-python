from src.dataimport.known_jobs_tsv_importer import KnownJobsImporter
from src.classifier.jobtitle.jobtitle_fts_classifier import JobtitleFtsClassifier
from src.util.jobtitle_util import count_variant, create_variants

tag_weight = {
    'h1': 0.6,
    'h2': 0.3,
    'h3': 0.1,
    'default': 0.1
}


# {
#   'job_1': [
#       'job_variant_1': {'h1': 10, 'h2': 5}
#       'job_variant_2': {'h2': 6}
#    ]
# }
def extract_features(tags, job_name_variants):
    features = {}
    for job_name, variants in job_name_variants:
        for tag in tags:
            tag_name = tag.name if tag.name else 'default'
            for variant, count in count_variants(tag.getText(), variants):
                if job_name not in features:
                    features[job_name] = {}
                if variant not in features[job_name]:
                    features[job_name][variant] = {}
                if tag_name not in features[job_name][variant]:
                    features[job_name][variant][tag_name] = 0
                features[job_name][variant][tag_name] += count
    return features


def count_variants(string, variants):
    for variant in (variant for variant in variants if variant in string):
        count = count_variant(variant, string)
        if count > 0:
            yield (variant, count)


class FeatureBasedJobtitleFtsClassifier(JobtitleFtsClassifier):
    def __init__(self, args, preprocessor):
        super(FeatureBasedJobtitleFtsClassifier, self).__init__(args, preprocessor)
        self.job_name_variants = [(job_name, create_variants(job_name)) for job_name in KnownJobsImporter()]

    def extract(self, tags):
        features = extract_features(tags, self.job_name_variants)
        best_match = None
        best_job_score = 0
        best_job_diversity = 0
        for job_name, job_stats in features.items():
            job_score = 0
            job_diversity = len(job_stats.items())

            best_variant = None
            best_variant_score = 0
            best_variant_length = 0
            for variant_name, variant_stats in job_stats.items():
                for tag_name, tag_count in variant_stats.items():
                    variant_score = self.calculate_score(tag_name, tag_count)
                    if variant_score > best_variant_score \
                            or variant_score == best_variant_score and len(variant_name) > best_variant_length:
                        best_variant_score = variant_score
                        best_variant = variant_name
                    if len(variant_name) > best_variant_length:
                        best_variant_length = len(variant_name)

                    job_score += variant_score
                    if job_score > best_job_score \
                            or job_score == best_job_score and job_diversity > best_job_diversity:
                        best_job_score = job_score
                        best_match = best_variant
                        if job_diversity > best_job_diversity:
                            best_job_diversity = job_diversity
        return best_match

    def normalize(self, score):
        if score < 1:
            return score
        return 1 / score

    def calculate_score(self, tag, count):
        score = 0
        key = tag if tag in tag_weight else 'default'
        score += tag_weight[key] * count
        # todo: add more feature values here if available
        return score
        # return self.normalize(score)

    def title(self):
        return 'Jobtitle Extractor: FTS (html-tag-based)'

    def description(self):
        return """Extract a jobtitle by performing a full text search (FTS) on the DOM. The text of the DOM is searched
        for occurrences of known job titles, including variants (such as male/female form, hyphenated forms etc...).
        The found results are then weighted according to the following criteria:
        - what HTML tag does the result appear in (h1 tags are considered more important than h2 tags and so on)
        - How often does the job title (including variants) appear in the DOM? Higher occurrence means higher probability
        that the result is the actual job title of the vacancy
        - in how many variants does the job title appear?
        """

    def label(self):
        return 'jobtitle-jobtitle-html-tags'
