import datetime
import os
import re
import time

from src.classifier.classifier import data_dir

date_pattern = '%Y-%m-%d-%H-%M-%S'


def create_filename(num_features, min_word_count, context):
    fn_ts = time.strftime(date_pattern)
    fn_parms = '{features}features_{minwords}minwords_{context}context'.format(features=num_features,
                                                                               minwords=min_word_count,
                                                                               context=context)
    filename = fn_ts + '_' + fn_parms
    return os.path.join(data_dir, filename)


def parse_filename(filename):
    patterns = {
        'datetime': r'(\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2})',
        'num_words': r'((\d*)words)',
        'num_features': r'((\d*)features)',
        'num_minwords': r'((\d*)minwords)',
        'num_context': r'((\d*)context)'
    }
    parms = {
        'datetime': None,
        'num_words': None,
        'num_features': None,
        'num_minwords': None,
        'num_context': None
    }
    pattern = r'_'.join(patterns.values())
    matches = re.findall(pattern, filename)
    for i, match in enumerate(match for match in matches[0] if matches):
        if i == 0:
            str = re.match(patterns['datetime'], match).string
            parms['datetime'] = datetime.datetime.strptime(str, date_pattern)
        elif i == 2:
            parms['num_words'] = int(match)
        elif i == 4:
            parms['num_features'] = int(match)
        elif i == 6:
            parms['num_minwords'] = int(match)
        elif i == 8:
            parms['num_context'] = int(match)

    return parms
