from functools import total_ordering

tag_weights = ['h1', 'h2', 'h3', 'strong', 'default']


def calculate_tag_weight(tag):
    key = tag if tag in tag_weights else 'default'
    return tag_weights.index(key)


@total_ordering
class JobtitleFtsFeatures(object):
    """helper class to sort features"""

    def __init__(self, job_name, highest_tag, first_position, num_occurrences, num_variants):
        self.job_name = job_name
        self.tag = highest_tag
        # lower tag weight means better
        self.tag_weight = calculate_tag_weight(highest_tag)
        # lower position means better
        self.first_position = first_position
        # higher number of occurrences means better
        self.num_occurrences = num_occurrences
        # higher number of variants means better
        self.num_variants = num_variants

    def __lt__(self, other):
        # note: The order of the attributes defines the sorting priority!
        return (self.tag_weight, -self.num_occurrences, self.first_position, -self.num_variants) < \
               (other.tag_weight, -other.num_occurrences, other.first_position, -other.num_variants)

    def __eq__(self, other):
        return (self.job_name, self.tag_weight, self.first_position, self.num_occurrences, self.num_variants) == \
               (other.job_name, other.tag_weight, other.first_position, other.num_occurrences, other.num_variants)
