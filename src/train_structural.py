import logging
import sys

from src.importer import import_all
from src.stats import print_stats

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def process_structure(row):
    dom = row['dom']
    sentences = tokenize_sentences(dom)
    words = tokenize_words(dom)


def tokenize_sentences(dom):
    pass


def tokenize_words(dom):
    pass


if __name__ == '__main__':
    stats = (process_structure(row) for row in import_all())
    print_stats(stats)
