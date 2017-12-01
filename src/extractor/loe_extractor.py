import logging
import re

from src.extractor.extractor import Extractor
from src.util import util

log = logging.getLogger(__name__)

p1 = '(\d\d\d?%?)-?(\d\d\d?%?)?'
p2 = '(\d\d\d?%?-\d\d\d?%?)|(\d\d\d?%?)'
p3 = '\d\d\d?%?-\d\d\d?%?|\d\d\d?%?'
LOE_PATTERN = re.compile(p3)


def group_tags_with_loe_patterns(tags):
    for tag in tags:
        results = find_loe_patterns(tag.getText())
        for result in results:
            yield (result, tag.name)


def find_loe_patterns(text):
    return LOE_PATTERN.findall(text)


class LoeExtractor(Extractor):
    def extract(self, tags):
        tags_with_numbers = group_tags_with_loe_patterns(tags)
        return None

    def title(self):
        return 'LoE Extractor'

    def description(self):
        return 'extract level of employment by performing a full text search (FTS) for certain patterns'

    def label(self):
        return 'loe-extractor'
