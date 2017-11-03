import argparse
import logging
import os
import pickle
import sys

import nltk
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
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

data_dir = 'D:/code/ip7-python/resource/semantic'
file_vectorizer = os.path.join(data_dir, 'vectorizer.pkl')
file_train_features = os.path.join(data_dir, 'train_features.pkl')
file_test_features = os.path.join(data_dir, 'test_features.pkl')
file_train_labels = os.path.join(data_dir, 'train_labels.pkl')
file_test_labels = os.path.join(data_dir, 'test_labels.pkl')
file_clf_random_forest = os.path.join(data_dir, 'clf_random_forest.pkl')


def preprocess(labeled_data):
    with labeled_data as data:
        for row in (row for row in tqdm(data, total=data.num_rows, unit=' rows') if row['html']):
            relevant_tags = preproc.preprocess(row['html'])
            vacancy_text = ' '.join((tag.getText() for tag in relevant_tags))
            words = preproc.remove_stop_words(vacancy_text)
            if len(words) > 0:
                yield words, row['title']


max_features = 500
train_size = 0.01
test_size = 0.1
data_train = LabeledData(split_from=0, split_to=train_size)
data_test = LabeledData(split_from=train_size, split_to=train_size + test_size)


def create_train_data(vectorizer):
    if args.rebuild or not os.path.isfile(file_train_features):
        logging.info('loading/cleaning training data from DB...')
        train_data = []
        train_labels = []
        for data, label in preprocess(data_train):
            train_data.append(data)
            train_labels.append(label)

        logging.info('created {} training elements with {} labels'.format(len(train_data), len(train_labels)))
        logging.info('creating training features from cleaned training data...')
        train_features = vectorizer.fit_transform(train_data)
        train_features = train_features.toarray()

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
        test_data = []
        test_labels = []
        for data, label in preprocess(data_test):
            test_data.append(data)
            test_labels.append(label)

        logging.info('created {} test elements with {} labels'.format(len(test_data), len(test_labels)))
        logging.info('creating test features from cleaned training data...')
        test_features = vectorizer.transform(test_data)

        logging.info('saving {}x{} features and vectorizer to file'.format(test_features.shape[0],
                                                                           test_features.shape[1]))
        pickle.dump(test_features, open(file_test_features, 'wb'))
        pickle.dump(test_labels, open(file_test_labels, 'wb'))
        return test_features, test_labels
    else:
        logging.info('Loading test features from file...')
        test_features = pickle.load(open(file_test_features, 'rb'))
        test_labels = pickle.load(open(file_test_labels, 'rb'))
        return test_features, test_labels


def create_vectorizer(args):
    if args.rebuild or not os.path.isfile(file_vectorizer):
        logging.info('recreating vectorizer...')
        return CountVectorizer(analyzer="word",
                               tokenizer=None,
                               preprocessor=None,
                               stop_words=None,
                               max_features=max_features
                               )
    else:
        logging.info('loading vectorizer from file...')
        return pickle.load(open(file_vectorizer, 'rb'))


def train_random_forest():
    if os.path.exists(file_clf_random_forest):
        logging.info('Loading RandomForestClassifier from file')
        return pickle.load(open(file_clf_random_forest, 'rb'))

    logging.info('Training new RandomForestClassifier')
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(train_features, train_labels)
    pickle.dump(clf, open(file_clf_random_forest, 'wb'))
    return clf


if __name__ == '__main__':
    # create test/training data
    logging.info('Creating training data')
    vectorizer = create_vectorizer(args)
    train_features, train_labels = create_train_data(vectorizer)

    # train classifier
    forest = train_random_forest()

    # make predictions
    test_features, test_labels = create_test_data(vectorizer)
    logging.info('using trained RandomForestClassifier to predict test features')
    predictions = forest.predict(test_features)

    # evaluate predictions
    logging.info('measuring accuracy of predictions')
    accuracy = accuracy_score(test_labels, predictions)
    logging.info(accuracy)
