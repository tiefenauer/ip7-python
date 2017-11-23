import logging

from src.importer import import_all
from src.util.boot_util import log_setup
from src.util.stats import print_stats

log_setup()
log = logging.getLogger(__name__)


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
