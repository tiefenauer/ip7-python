import collections
import logging
import operator
import re

from src.classifier.fts_classifier import FtsClassifier
from src.classifier.loe.loe_classifier import LoeClassifier

log = logging.getLogger(__name__)

# matches any pattern, hyphenated or not
LOE_PATTERN = re.compile('\d\d\d?\s*%?\s*-\s*\d\d\d?\s*%?|\d\d\d?\s*%?')
# matches single LOE: 80%, 100%, ... (arbitrary number of spaces before percent sign
LOE_PATTERN_SINGLE = re.compile('\d\d\d?\s*%')
# matches LOE range: 60(%)-80%, 70(%)-100% ... (first percent symbol is optional)
LOE_PATTERN_RANGE = re.compile('\d\d\d?\s*%?\s*-\s*\d\d\d?\s*%')

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
        matches = group_loe_patterns_by_count(tags)
        workquota_min = 100
        workquota_max = 100
        if matches:
            loe = matches[0][0]
            if re.match(LOE_PATTERN_SINGLE, loe):
                workquota_min = re.sub('\s*%', '', loe)
                workquota_max = workquota_min
            if re.match(LOE_PATTERN_RANGE, loe):
                workquota_min, workquota_max = loe.split('-')
            workquota_min = re.sub('\s*%', '', workquota_min)
            workquota_max = re.sub('\s*%', '', workquota_max)

        return int(workquota_min), int(workquota_max)

    def title(self):
        return 'LoE Extractor'

    def label(self):
        return 'extract_loe'
