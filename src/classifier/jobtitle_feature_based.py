from src.classifier.classification_strategy import ClassificationStrategy
from src.importer.job_name_importer import JobNameImporter
from src.util.jobtitle_util import count_variant, create_variants

job_name_variants = list((job_name, create_variants(job_name)) for job_name in JobNameImporter())
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
def extract_features(tags, job_name_variants=job_name_variants):
    features = {}
    for job_name, variants in job_name_variants:
        for tag in tags:
            tag_name = tag.name if tag.name else 'default'
            for variant, count in extract_variants(tag.getText(), variants):
                if job_name not in features:
                    features[job_name] = {}
                if variant not in features[job_name]:
                    features[job_name][variant] = {}
                if tag_name not in features[job_name][variant]:
                    features[job_name][variant][tag_name] = 0
                features[job_name][variant][tag_name] += count
    return features


def extract_variants(string, variants):
    for variant in (variant for variant in variants if variant in string):
        count = count_variant(variant, string)
        if count > 0:
            yield (variant, count)


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

    def classify(self, tags):
        features = extract_features(tags, job_name_variants)
        best_variant_score = 0
        best_variant = None
        best_job_count = 0
        best_job_variants = None
        best_job_diversity = 0
        for job_name, job_stats in features.items():
            job_count = 0
            job_diversity = len(job_stats.items())
            for variant_name, variant_stats in job_stats.items():
                for tag_name, tag_count in variant_stats.items():
                    job_count += tag_count

            if job_count > best_job_count or job_count == best_job_count and job_diversity > best_job_diversity:
                best_job_count = job_count
                best_job_variants = job_stats
            if job_diversity > best_job_diversity:
                best_job_diversity = job_diversity
        best_score = 0
        best_match = None
        for variant_name, variant_stats in best_job_variants.items():
            for tag, count in variant_stats.items():
                score = self.calculate_score(tag, count)
                if score > best_score:
                    best_score = score
                    best_match = variant_name
        return best_match

    def calculate_score(self, tag, count):
        score = 0
        key = tag if tag in tag_weight else 'default'
        score += count * tag_weight[key]
        # todo: add more feature values here if available
        return score
        # return self.normalize(score)

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
