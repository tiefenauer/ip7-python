import logging
import re

from src.classifier.loe.loe_classifier import LoeClassifier
from src.classifier.loe.loe_fts_features import LoeFtsFeatures
from src.classifier.tag_classifier import TagClassifier
from src.util import loe_util

log = logging.getLogger(__name__)


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
            lst.append(LoeFtsFeatures(p, t, c))

    # step 4a: perform some filtering
    # filter out items without percent in pattern (those are unlikely to be LOE)
    lst = (loe for loe in lst if '%' in loe.pattern)
    # filter out items that occur in lists (those are more likely to belong to skills etc.)
    lst = (loe for loe in lst if loe.tag_name not in ['li', 'ul', 'ol'])
    # step 4b: sort list by pattern suffix ASC (percentages first), tag weight ASC (according to tag_order), count DESC
    sorted_lst = sorted(lst, key=lambda x: (x.ends_with_percent, x.tag_weight, -x.count))
    # step 5: convert list to 3-tupel
    result = []
    for loe in sorted_lst:
        result.append((loe.pattern, loe.tag_name, loe.count))

    return result


def find_loe_patterns_by_tag(tags):
    for tag in tags:
        for result in loe_util.find_all_loe(tag.getText()):
            yield result, tag.name


class LoeFtsClassifier(TagClassifier, LoeClassifier):
    """Predict level of employment (LOE) by performing a full text search (FTS) on the processed data for numeric
    information."""

    def predict_class(self, tags):
        matches = group_loe_patterns_by_count(tags)
        workquota_min = '100'
        workquota_max = '100'
        if matches:
            loe = matches[0][0]
            if loe_util.is_single_percentage(loe):
                workquota_min = re.sub('\s*%', '', loe)
                workquota_max = workquota_min
            if loe_util.is_percentate_range(loe):
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
