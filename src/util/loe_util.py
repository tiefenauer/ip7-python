import re

# matches any pattern, hyphenated or not
LOE_PATTERN = re.compile('\d\d\d?\s*%?\s*-\s*\d\d\d?\s*%?|\d\d\d?\s*%?')
# matches single LOE: 80%, 100%, ... (arbitrary number of spaces before percent sign
LOE_PATTERN_SINGLE = re.compile('\d\d\d?\s*%')
# matches LOE range: 60(%)-80%, 70(%)-100% ... (first percent symbol is optional)
LOE_PATTERN_RANGE = re.compile('\d\d\d?\s*%?\s*-\s*\d\d\d?\s*%')


def is_single_percentage(text):
    return bool(re.match(LOE_PATTERN_SINGLE, text))


def is_percentate_range(text):
    return bool(re.match(LOE_PATTERN_RANGE, text))


def find_all_loe(text):
    return (loe.strip() for loe in LOE_PATTERN.findall(text))


def remove_percentage(text):
    return re.sub(LOE_PATTERN, '', text).strip()
