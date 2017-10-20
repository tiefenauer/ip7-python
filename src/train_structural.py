import logging
import sys

from src.job_importer import process_stream

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



def process_structure(row):
    dom = row['dom']
    sentences = tokenize_sentences(dom)
    words = tokenize_words(dom)


def tokenize_sentences(dom):
    pass


def tokenize_words(dom):
    pass


process_stream(process_structure)
