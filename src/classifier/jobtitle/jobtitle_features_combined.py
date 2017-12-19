from functools import total_ordering

tag_weights = ['title', 'h1', 'h2', 'h3', 'strong', 'default']
origin_weights = ['known-job', 'mw', 'loe', 'default']


def calculate_tag_weight(tag):
    return calculate_weight(tag, tag_weights)


def calculate_origin_weight(origin):
    return calculate_weight(origin, origin_weights)


def calculate_weight(item, weights):
    key = item if item in weights else 'default'
    return weights.index(key)


@total_ordering
class JobtitleFeaturesCombined(object):
    """helper class to sort features"""

    def __init__(self, tag_position, job_name, html_tag, origin):
        self.tag_position = tag_position
        self.job_name = job_name
        self.html_tag = html_tag
        self.origin = origin
        # lower tag weight means better
        self.tag_weight = calculate_tag_weight(html_tag)
        # lower origin weight means better
        self.origin_weight = calculate_origin_weight(origin)
        # longer job name means better
        self.job_name_length = -len(job_name)

    def __lt__(self, other):
        # note: The order of the attributes defines the sorting priority!
        return (self.tag_weight, self.tag_position, self.origin_weight, self.job_name_length) < \
               (other.tag_weight, other.tag_position, other.origin_weight, other.job_name_length)

    def __eq__(self, other):
        return (self.tag_position, self.job_name, self.html_tag, self.origin_weight) == \
               (other.tag_position, other.job_name, other.html_tag, other.origin_weight)
