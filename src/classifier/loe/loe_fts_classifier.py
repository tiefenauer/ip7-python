import collections
import logging
import operator
import re

from src.classifier.fts_classifier import FtsClassifier
from src.classifier.loe.loe_classifier import LoeClassifier

log = logging.getLogger(__name__)

p1 = '(\d\d\d?%?)-?(\d\d\d?%?)?'
p2 = '(\d\d\d?%?-\d\d\d?%?)|(\d\d\d?%?)'
p3 = '\d\d\d?%?-\d\d\d?%?|\d\d\d?%?'
LOE_PATTERN = re.compile(p3)

tag_order = ['h1', 'h2', 'h3', 'p']


def group_loe_patterns_by_tag(tags):
    # TODO: this method does not work as expected
    patterns_by_tag = find_loe_patterns_by_tag(tags)
    patterns_by_tag = list(patterns_by_tag)
    d = collections.defaultdict(list)
    for (pattern, tag_name) in patterns_by_tag:
        d[pattern].append(tag_name)

    result = []
    for (pattern, tag_list) in d.items():
        seen = set()
        for tag_name in (tag_name for tag_name in tag_list if not (tag_name in seen or seen.add(tag_name))):
            result.append((pattern, tag_name, tag_list.count(tag_name)))

    # sort by html tag
    result = sorted(result, key=lambda item: tag_order.index(item[1]) if item[1] in tag_order else 999)
    result = sorted(result, key=operator.itemgetter(1, 2), reverse=True)
    result = sorted(result, key=operator.itemgetter(0))
    # result = sorted(result, key=lambda item: (item[2], -item[2]), reverse=True)
    return result


def group_loe_patterns_by_count(tags):
    patterns_by_tag = find_loe_patterns_by_tag(tags)
    dct = {}
    for pattern, tag in patterns_by_tag:
        if pattern not in dct: dct[pattern] = 0
        dct[pattern] += 1
    return sorted(dct.items(), key=operator.itemgetter(1), reverse=True)


def find_loe_patterns_by_tag(tags):
    for tag in tags:
        results = find_loe_patterns(tag.getText())
        for result in results:
            yield (result, tag.name)


def find_loe_patterns(text):
    return LOE_PATTERN.findall(text)


class LoeFtsClassifier(FtsClassifier, LoeClassifier):
    """Predict level of employment (LOE) by performing a full text search (FTS) on the processed data for numeric
    information."""

    def classify(self, tags):
        tags_with_numbers = group_loe_patterns_by_count(tags)
        if len(tags_with_numbers) > 0:
            return tags_with_numbers[0][0]
        return None

    def title(self):
        return 'LoE Extractor'

    def label(self):
        return 'extract_loe'
