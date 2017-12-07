import logging
import re
from functools import total_ordering

from src.classifier.fts_classifier import FtsClassifier
from src.classifier.loe.loe_classifier import LoeClassifier

log = logging.getLogger(__name__)

# matches any pattern, hyphenated or not
LOE_PATTERN = re.compile('\d\d\d?\s*%?\s*-\s*\d\d\d?\s*%?|\d\d\d?\s*%?')
# matches single LOE: 80%, 100%, ... (arbitrary number of spaces before percent sign
LOE_PATTERN_SINGLE = re.compile('\d\d\d?\s*%')
# matches LOE range: 60(%)-80%, 70(%)-100% ... (first percent symbol is optional)
LOE_PATTERN_RANGE = re.compile('\d\d\d?\s*%?\s*-\s*\d\d\d?\s*%')

tag_order = ['h*', 'strong', 'p']


@total_ordering
class LoeOccurrence(object):
    """helper class to sort occurrences of LOE"""

    def __init__(self, pattern, html_tag, count):
        # LOE occurrence metadata
        self.pattern = pattern
        self.tag = html_tag
        self.count = count

        # attributes for sorting
        self.ends_with_percent = 0 if '%' in pattern else 1
        self.tag_weight = tag_order.index(html_tag[:1]) \
            if html_tag \
               and len(html_tag) > 0 \
               and html_tag in tag_order \
            else len(tag_order) + 1

    def __lt__(self, other):
        return ((self.ends_with_percent, self.tag_weight, self.count) <
                (other.ends_with_percent, other.tag_weight, other.count))

    def __eq__(self, other):
        return ((self.ends_with_percent, self.tag_weight, self.count) ==
                (other.ends_with_percent, other.tag_weight, other.count))


def group_loe_patterns_by_count(tags):
    """creates a list of triples of format (LOE, HTML-Tag, Count)
    The list is sorted by (in this order)
    - LOE pattern  ASC: patterns with percent symbol before patterns without percent symbol
    - HTML-Tag priority AS: higher priority before lower prioritiy (lower number=higher priority)
    - Count DESC: more frequent patterns before less frequent patterns
    """
    # step 1: map patterns to HTML tags
    patterns_by_tag = find_loe_patterns_by_tag(tags)
    # step 2: count occurrence of each mapping pattern -> HTML-Tag
    dct = {}
    for pattern, html_tag in patterns_by_tag:
        if pattern not in dct: dct[pattern] = dict()
        if pattern in dct and html_tag not in dct[pattern]: dct[pattern][html_tag] = 0
        dct[pattern][html_tag] += 1

    # step 3: convert to sortable Items
    lst = []
    for p in dct:
        for t in dct[p]:
            c = dct[p][t]
            lst.append(LoeOccurrence(p, t, c))

    # step 4a: perform some filtering
    # filter out items without percent in pattern (those are unlikely to be LOE)
    lst = (loe for loe in lst if '%' in loe.pattern)
    # filter out items that occur in lists (those are more likely to belong to skills etc.)
    lst = (loe for loe in lst if loe.tag not in ['li', 'ul', 'ol'])
    # step 4b: sort list by pattern suffix ASC (percentages first), tag weight ASC (according to tag_order), count DESC
    sorted_lst = sorted(lst, key=lambda x: (x.ends_with_percent, x.tag_weight, -x.count))
    # step 5: convert list to 3-tupel
    result = []
    for loe in sorted_lst:
        result.append((loe.pattern, loe.tag, loe.count))

    return result


def find_loe_patterns_by_tag(tags):
    for tag in tags:
        results = LOE_PATTERN.findall(tag.getText())
        for result in results:
            yield (result.strip(), tag.name)


class LoeFtsClassifier(FtsClassifier, LoeClassifier):
    """Predict level of employment (LOE) by performing a full text search (FTS) on the processed data for numeric
    information."""

    def classify(self, tags):
        matches = group_loe_patterns_by_count(tags)
        workquota_min = '100'
        workquota_max = '100'
        if matches:
            loe = matches[0][0]
            if re.match(LOE_PATTERN_SINGLE, loe):
                workquota_min = re.sub('\s*%', '', loe)
                workquota_max = workquota_min
            if re.match(LOE_PATTERN_RANGE, loe):
                workquota_min, workquota_max = loe.split('-')
            workquota_min = re.sub('\s*%', '', workquota_min)
            workquota_max = re.sub('\s*%', '', workquota_max)

        try:
            workquota_min = int(workquota_min)
        except:
            workquota_min = 100
        try:
            workquota_max = int(workquota_max)
        except:
            workquota_max = 100
        return workquota_min, workquota_max

    def title(self):
        return 'LoE FTS-Classifier'

    def label(self):
        return 'loe-fts'
