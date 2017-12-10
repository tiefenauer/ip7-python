from functools import total_ordering

tag_ordering = ['h*', 'strong', 'p']


def calculate_tag_weight(tag_name):
    if tag_name and len(tag_name) == 2 and tag_name[:1] + '*' in tag_ordering:
        return tag_ordering.index(tag_name[:1] + '*')
    return tag_ordering.index(tag_name) if tag_name in tag_ordering else len(tag_ordering) + 1


@total_ordering
class LoeFtsFeatures(object):
    """helper class to sort occurrences of LOE"""

    def __init__(self, pattern, tag_name, count):
        # metadata
        self.pattern = pattern
        self.tag_name = tag_name
        self.count = count

        # attributes for sorting
        self.ends_with_percent = 0 if '%' in pattern else 1
        self.tag_weight = calculate_tag_weight(tag_name)

    def __lt__(self, other):
        return ((self.ends_with_percent, self.tag_weight, self.count) <
                (other.ends_with_percent, other.tag_weight, other.count))

    def __eq__(self, other):
        return ((self.ends_with_percent, self.tag_weight, self.count) ==
                (other.ends_with_percent, other.tag_weight, other.count))
