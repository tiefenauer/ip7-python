import re

from src.classifier.classification_strategy import ClassificationStrategy
from src.importer.job_name_importer import JobNameImporter
from src.util import jobtitle_util
from src.util.jobtitle_util import count_variant


def create_job_name_spaced(job_name_1, job_name_2):
    return job_name_1 + ' ' + job_name_2


def create_job_name_concatenated(job_name_1, job_name_2):
    return job_name_1 + job_name_2


def create_job_name_hyphenated(job_name_1, job_name_2):
    return job_name_1 + '-' + job_name_2


hyphenated_pattern = re.compile('(?=\S*[-])([a-zA-Z-]+)')


def is_hyphenated(job_name):
    return hyphenated_pattern.match(job_name)


def create_write_variants(job_name):
    write_variants = set()
    write_variants.add(job_name)
    if is_hyphenated(job_name):
        job_name_parts = re.findall('([a-zA-Z]+)', job_name)
        part1 = job_name_parts[0]
        part2 = job_name_parts[1]
        job_concatenated = create_job_name_concatenated(part1, part2.lower())
        job_spaced = create_job_name_spaced(part1, part2)
        write_variants.add(job_concatenated)
        write_variants.add(job_spaced)
    else:
        for known_job in JobNameImporter():
            if known_job.lower() in job_name:
                part1 = job_name.split(known_job.lower())[0].strip()
                job_concatenated = create_job_name_concatenated(part1, known_job.lower())
                job_spaced = create_job_name_spaced(part1, known_job)
                job_hyphenated = create_job_name_hyphenated(part1, known_job)
                write_variants.add(job_concatenated)
                write_variants.add(job_spaced)
                write_variants.add(job_hyphenated)

    return write_variants


def create_gender_variants(job_name):
    job_variants = jobtitle_util.create_variants(job_name)
    return job_variants


def create_writing_and_gender_variants(job_name):
    variants = set()
    write_variants = create_write_variants(job_name)
    variants.update(write_variants)
    for write_variant in write_variants:
        gender_variants = create_gender_variants(write_variant)
        variants.update(gender_variants)

    return variants


job_name_variants = list((job_name, create_writing_and_gender_variants(job_name))
                     for job_name in JobNameImporter())
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

    def calculate_score(self, tag, count):
        score = 0
        key = tag if tag in tag_weight else 'default'
        score += tag_weight[key] * count
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
