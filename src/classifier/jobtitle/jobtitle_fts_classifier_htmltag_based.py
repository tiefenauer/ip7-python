import math

from src.classifier.jobtitle import jobtitle_fts_features
from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.jobtitle.jobtitle_fts_features import JobtitleFtsFeatures
from src.classifier.tag_classifier import TagClassifier
from src.dataimport.known_jobs import KnownJobs
from src.util.jobtitle_util import count_variant, create_variants


# {


#   'job_1': [
#       'job_variant_1': {'h1': 10, 'h2': 5}
#       'job_variant_2': {'h2': 6}
#    ]
# }
def create_statistics(tags, job_name_variants):
    """extracts stats about where and how often job names and/or their variants occur in a given
    @tags: a set of tags
    @job_name_variants: map 'job_name' -> ['variant1', 'variant2', ...]
    """
    features = {}
    for job_name, variants in job_name_variants:
        for tag_pos, tag in enumerate(tags):
            tag_name = tag.name if tag.name else 'default'
            for variant, count in count_variants(tag.getText(), variants):
                if job_name not in features:
                    features[job_name] = {}
                if variant not in features[job_name]:
                    features[job_name][variant] = {}
                if tag_name not in features[job_name][variant]:
                    features[job_name][variant][tag_name] = []
                features[job_name][variant][tag_name].append({'tag_pos': tag_pos, 'count': count})
    return features


def count_variants(text, variants):
    """counts all occurrences of the job variants in a text string"""
    for variant in (variant for variant in variants if variant.lower() in text.lower()):
        count = count_variant(variant.lower(), text.lower())
        if count > 0:
            yield (variant, count)


def create_fts_features(features):
    feature_list = []
    for job_name in features:
        num_variants = 0
        num_occurrences = 0
        first_position = math.inf
        lowest_tag_weight = math.inf
        highest_tag = None

        for job_variant in features[job_name]:
            num_variants += 1
            for tag_name in features[job_name][job_variant]:
                tag_weight = jobtitle_fts_features.calculate_tag_weight(tag_name)
                if tag_weight < lowest_tag_weight:
                    lowest_tag_weight = tag_weight
                    highest_tag = tag_name
                for pos_count in features[job_name][job_variant][tag_name]:
                    position = pos_count['tag_pos']
                    count = pos_count['count']
                    if position < first_position:
                        first_position = position
                    num_occurrences += count

        feature_list.append(JobtitleFtsFeatures(job_name, highest_tag, first_position, num_occurrences, num_variants))
    return feature_list


job_name_variants = [(job_name, create_variants(job_name)) for job_name in KnownJobs()]


# with db_session:
#     job_name_variants = [(job_class.job_name, set(variant.job_name_variant for variant in job_class.variants))
#                          for job_class in Job_Class.select()]


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

    def classify(self, tags):
        stats = create_statistics(tags, job_name_variants)
        features = create_fts_features(stats)
        if len(features) > 0:
            best_match = sorted(features)[0]
            return best_match.job_name
        return None

    def title(self):
        return 'Jobtitle Classifier: FTS (html-tag-based)'

    def label(self):
        return 'jobtitle-fts-html-tags'
