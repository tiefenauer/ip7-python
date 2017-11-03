import argparse
import logging
import os
import pickle
import sys

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm

from src import preproc
from src.importer.data_labeled import LabeledData

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('-r', '--rebuild', help='force rebuild vocabulary')
args = parser.parse_args()

sentence_detector = nltk.data.load('tokenizers/punkt/german.pickle')

file_vectorizer = os.path.join('D:/code/ip7-python/resource', 'semantic_vector.pkl')


def preprocess(labeled_data):
    with labeled_data as data:
        for row in (row for row in tqdm(data, total=data.num_rows, unit=' rows') if row['html']):
            relevant_tags = preproc.preprocess(row['html'])
            vacancy_text = ' '.join((tag.getText() for tag in relevant_tags))
            sentences = sentence_detector.tokenize(vacancy_text)
            for sentence in sentences:
                words = nltk.word_tokenize(sentence)
                for word in words:
                    yield word


def generate_clean_train_data():
    return preprocess(LabeledData(offset=0, limit=0.5))


def generate_clean_test_data():
    return preprocess(LabeledData(offset=0.5, limit=1))


def rebuild_vocab():
    clean_train_data = generate_clean_train_data()
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=5000
                                 )
    vectorizer.fit_transform(clean_train_data)
    pickle.dump(vectorizer, open(file_vectorizer, 'wb'))
    return vectorizer


def create_vectorizer(args):
    if args.rebuild or not os.path.isfile(file_vectorizer):
        logging.info('rebuilding vectors...')
        return rebuild_vocab()
    else:
        logging.info('loading vectors from file...')
        return pickle.load(open(file_vectorizer, 'rb'))


if __name__ == '__main__':
    vectorizer = create_vectorizer(args)
    clean_test_data = generate_clean_test_data()
    vectorizer.transform(clean_test_data)
