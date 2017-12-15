from functools import total_ordering

tag_weights = ['h1', 'h2', 'h3', 'strong', 'default']


def calculate_tag_weight(tag):
    key = tag if tag in tag_weights else 'default'
    return tag_weights.index(key)


@total_ordering
class JobtitleFeaturesCombined(object):
    """helper class to sort features"""

    def __init__(self, tag_position, job_name, html_tag, tagged_words, job_positions):
        self.tag_position = tag_position
        self.job_name = job_name
        self.html_tag = html_tag
        self.tagged_words = tagged_words
        self.positions = job_positions
        # lower tag weight means better
        self.tag_weight = calculate_tag_weight(html_tag)
        # lower position means better
        self.min_job_position = min(job_positions)

    def __lt__(self, other):
        # note: The order of the attributes defines the sorting priority!
        return (self.tag_weight, self.tag_position, self.min_job_position) < \
               (other.tag_weight, other.tag_position, other.min_job_position)

    def __eq__(self, other):
        return (self.tag_position, self.job_name, self.html_tag, self.tagged_words, self.positions) == \
               (other.tag_position, other.job_name, other.html_tag, other.tagged_words, other.positions)


def create_features(tag_position, html_tag, variant, positions, tagged_words):
    return JobtitleFeaturesCombined()
