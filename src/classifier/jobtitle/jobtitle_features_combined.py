from functools import total_ordering

tag_weights = ['h1', 'h2', 'h3', 'strong', 'default']


def calculate_tag_weight(tag):
    key = tag if tag in tag_weights else 'default'
    return tag_weights.index(key)


@total_ordering
class JobtitleFeaturesCombined(object):
    """helper class to sort features"""

    def __init__(self, tag_position, job_name, html_tag):
        self.tag_position = tag_position
        self.job_name = job_name
        self.html_tag = html_tag
        # lower tag weight means better
        self.tag_weight = calculate_tag_weight(html_tag)

    def __lt__(self, other):
        # note: The order of the attributes defines the sorting priority!
        return (self.tag_weight, self.tag_position) < \
               (other.tag_weight, other.tag_position)

    def __eq__(self, other):
        return (self.tag_position, self.job_name, self.html_tag) == \
               (other.tag_position, other.job_name, other.html_tag)
