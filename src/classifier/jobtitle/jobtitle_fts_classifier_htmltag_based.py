import math

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.jobtitle.jobtitle_fts_features import JobtitleFtsFeatures, calculate_tag_weight
from src.classifier.tag_classifier import TagClassifier
from src.dataimport.known_job_variants import KnownJobVariants
from src.util.jobtitle_util import count_variant


def count_job_in_tags(tags, job_name_variants):
    return sum(count_job(tag, job_name_variants) for tag in tags)


def count_job(tag, job_name_variants):
    return sum(count for (variant, count) in count_variants(tag.getText(), job_name_variants))


def count_variants(text, variants):
    """counts all occurrences of the job variants in a text string"""
    for variant in (variant for variant in variants if variant in text):
        count = count_variant(variant, text)
        if count > 0:
            yield (variant, count)


known_job_variants = KnownJobVariants()


def calculate_highest_tag(tags, variants):
    highest_tag = None
    min_weight = math.inf
    for variant in variants:
        for tag_index, tag in enumerate(tag for tag in tags if variant in tag.getText()):
            tag_weight = calculate_tag_weight(tag.name)
            if tag_weight < min_weight:
                min_weight = tag_weight
                highest_tag = tag
    return highest_tag


def calculate_first_tag(tags, variants):
    for variant in variants:
        for tag_index, tag in enumerate(tags):
            if variant in tag.getText():
                return tag_index


class FeatureBasedJobtitleFtsClassifier(TagClassifier, JobtitleClassifier):
    """Predict a jobtitle by performing a full text search (FTS) on the processed data. The text of the processed data
     is searched for occurrences of known job names, including variants (such as male/female form, hyphenated forms
     etc...).
     The found results are then weighted according to the following criteria:
     - what HTML tag does the result appear in (h1 tags are considered more important than h2 tags and so on)
     - How often does the job title (including variants) appear in the DOM? Higher occurrence means higher probability
     that the result is the actual job title of the vacancy
     - in how many variants does the job title appear?
     """

    def predict_class(self, tags):
        tags = list(tags)
        features_list = []
        for job_name, variants in known_job_variants:
            job_name_count = count_job_in_tags(tags, variants)
            if job_name_count > 0:
                highest_tag = calculate_highest_tag(tags, variants)
                first_tag_index = calculate_first_tag(tags, variants)
                features = JobtitleFtsFeatures(job_name, highest_tag.name, first_tag_index, job_name_count)
                features_list.append(features)

        features_list = sorted(features_list)
        if len(features_list) > 0:
            best_match = sorted(features_list)[0]
            return best_match.job_name
        return None

    def title(self):
        return 'Jobtitle Classifier: FTS (html-tag-based)'

    def label(self):
        return 'jobtitle-fts-html-tags'
