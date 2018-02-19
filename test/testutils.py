import os

from src.util.globals import TEST_RESOURCE_DIR


def read_sample_file(filename):
    path = os.path.join(TEST_RESOURCE_DIR, filename + '.html')
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def write_extracted_tags(extracted_tags, filename):
    path = os.path.join(TEST_RESOURCE_DIR, filename + '.html')
    with open(path, 'w+', encoding='utf-8') as file:
        for tag in extracted_tags:
            file.write(str(tag) + '\n')


def write_markup(soup, filename):
    path = os.path.join(TEST_RESOURCE_DIR, filename + '.html')
    with open(path, 'w+', encoding='utf-8') as file:
        file.write(soup.prettify())


class DummyArgs(object):
    def __init__(self):
        self.split = None


def create_dummy_args(split=None):
    args = DummyArgs()
    args.split = split
    return args


class DummyRow(object):
    def __init__(self):
        self.html = None
        self.plaintext = None
        self.processed = []


def create_dummy_row(title=None, plaintext=None, html=None):
    row = DummyRow()
    row.title = title
    row.html = html
    row.plaintext = plaintext
    return row
