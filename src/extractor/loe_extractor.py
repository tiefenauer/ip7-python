import collections
import logging
import re

from src.extractor.extractor import Extractor

log = logging.getLogger(__name__)

p1 = '(\d\d\d?%?)-?(\d\d\d?%?)?'
p2 = '(\d\d\d?%?-\d\d\d?%?)|(\d\d\d?%?)'
p3 = '\d\d\d?%?-\d\d\d?%?|\d\d\d?%?'
LOE_PATTERN = re.compile(p3)


def group_loe_patterns_by_tag(tags):
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

    return result


def find_loe_patterns_by_tag(tags):
    for tag in tags:
        results = find_loe_patterns(tag.getText())
        for result in results:
            yield (result, tag.name)


def find_loe_patterns(text):
    return LOE_PATTERN.findall(text)


class LoeExtractor(Extractor):
    def extract(self, tags):
        tags_with_numbers = find_loe_patterns_by_tag(tags)
        return None

    def title(self):
        return 'LoE Extractor'

    def description(self):
        return 'extract level of employment by performing a full text search (FTS) for certain patterns'

    def label(self):
        return 'loe-extractor'
