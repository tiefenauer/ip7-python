import argparse
import logging
import os
import pickle
import sys

import nltk
from sklearn.ensemble import RandomForestClassifier
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

file_vectorizer = os.path.join('D:/code/ip7-python/resource/semantic', 'train_vectorizer_semantic.pkl')

file_train_features = os.path.join('D:/code/ip7-python/resource/semantic', 'train_features_semantic.pkl')
file_train_labels = os.path.join('D:/code/ip7-python/resource/semantic', 'train_labels_semantic.pkl')

file_test_features = os.path.join('D:/code/ip7-python/resource/semantic', 'test_features_semantic.pkl')


def preprocess(labeled_data):
    with labeled_data as data:
        for row in (row for row in tqdm(data, total=data.num_rows, unit=' rows') if row['html']):
            relevant_tags = preproc.preprocess(row['html'])
            vacancy_text = ' '.join((tag.getText() for tag in relevant_tags))
            words = preproc.remove_stop_words(vacancy_text)
            if len(words) > 0:
                yield words, row['title']


data_train = LabeledData(split_from=0, split_to=0.1)
data_test = LabeledData(split_from=0.1, split_to=1)


def generate_clean_train_data():
    return preprocess(data_train)


def generate_clean_test_data():
    return preprocess(data_test)


def create_train_data(vectorizer):
    if args.rebuild or not os.path.isfile(file_train_features):
        logging.info('loading/cleaning training data from DB...')
        training_tuples = generate_clean_train_data()
        train_data = []
        train_labels = []
        for data, label in training_tuples:
            train_data.append(data)
            train_labels.append(label)

        logging.info('created {} training elements with {} labels'.format(len(train_data), len(train_labels)))
        logging.info('creating training features from cleaned training data...')
        train_features = vectorizer.fit_transform(train_data)

        logging.info('saving {}x{} features and vectorizer to file'.format(train_features.shape[0],
                                                                           train_features.shape[1]))
        pickle.dump(vectorizer, open(file_vectorizer, 'wb'))
        pickle.dump(train_labels, open(file_train_labels, 'wb'))
        pickle.dump(train_features, open(file_train_features, 'wb'))
        return train_features, train_labels
    else:
        logging.info('Loading training features and labels from file...')
        train_data = pickle.load(open(file_train_features, 'rb'))
        train_labels = pickle.load(open(file_train_labels, 'rb'))
        return train_data, train_labels


def create_test_data(vectorizer):
    if args.rebuild or not os.path.isfile(file_test_features):
        logging.info('loading/cleaning test data from DB...')
        test_data = (data for (data, label) in generate_clean_test_data())
        test_features = vectorizer.transform(test_data)

        logging.info('saving {}x{} features to file'.format(train_features.shape[0],
                                                            train_features.shape[1]))
        pickle.dump(test_features, open(file_test_features, 'wb'))
        return test_features
    else:
        logging.info('Loading test features from file...')
        return pickle.load(open(file_test_features, 'rb'))


def create_vectorizer(args):
    if args.rebuild or not os.path.isfile(file_vectorizer):
        logging.info('recreating vectorizer...')
        return CountVectorizer(analyzer="word",
                               tokenizer=None,
                               preprocessor=None,
                               stop_words=None,
                               max_features=5000
                               )
    else:
        logging.info('loading vectorizer from file...')
        return pickle.load(open(file_vectorizer, 'rb'))


if __name__ == '__main__':
    # create training data with labels
    logging.info('Creating training data')
    vectorizer = create_vectorizer(args)
    train_features, train_labels = create_train_data(vectorizer)
    # train classifier
    forest = RandomForestClassifier(n_estimators=10)
    logging.info('Training RandomForestClassifier')
    forest.fit(train_features, train_labels)
    # evaluate classifier
    logging.info('using trained RandomForestClassifier to predict test features')
    test_features = create_test_data(vectorizer)
