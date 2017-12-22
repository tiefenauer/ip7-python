from functools import total_ordering

tag_weights = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'strong', 'default']


def calculate_tag_weight(tag_name):
    key = tag_name if tag_name in tag_weights else 'default'
    return tag_weights.index(key)


@total_ordering
class JobtitleFtsFeatures(object):
    """helper class to sort features"""

    def __init__(self, job_name, highest_tag_name, first_tag_index, job_name_count):
        self.job_name = job_name
        self.highest_tag_name = highest_tag_name
        # lower tag weight means better
        self.tag_weight = calculate_tag_weight(highest_tag_name)
        # lower position means better
        self.first_tag_index = first_tag_index
        # higher number of occurrences means better
        self.job_name_count = -job_name_count

    def __lt__(self, other):
        # note: The order of the attributes defines the sorting priority!
        return (self.tag_weight, self.job_name_count, self.first_tag_index) < \
               (other.tag_weight, other.job_name_count, other.first_tag_index)

    def __eq__(self, other):
        return (self.job_name, self.tag_weight, self.first_tag_index, self.job_name_count) == \
               (other.job_name, other.tag_weight, other.first_tag_index, other.job_name_count)
