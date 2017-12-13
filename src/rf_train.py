import argparse
import logging
import os
import pickle

import nltk
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm

from src.preprocessing import preproc
from src.database.X28TestData import X28TestData
from src.database.X28TrainData import X28TrainData
from src.evaluation.jobtitle.jobtitle_classification_scorer_linear import LinearJobtitleClassificationScorer
from src.evaluation.jobtitle.jobtitle_classification_scorer_strict import StrictJobtitleClassificationScorer
from src.evaluation.jobtitle.jobtitle_classification_scorer_tolerant import TolerantJobtitleClassificationScorer
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('-r', '--rebuild', help='force rebuild vocabulary')
args = parser.parse_args()

sentence_detector = nltk.data.load('tokenizers/punkt/german.pickle')

data_dir = 'D:/code/ip7-python/resource/models/randomforest'
file_vectorizer = os.path.join(data_dir, 'vectorizer.pkl')
file_train_features = os.path.join(data_dir, 'train_features.pkl')
file_test_features = os.path.join(data_dir, 'test_features.pkl')
file_train_labels = os.path.join(data_dir, 'train_labels.pkl')
file_test_labels = os.path.join(data_dir, 'test_labels.pkl')
file_clf_random_forest = os.path.join(data_dir, 'clf_random_forest.pkl')


def preprocess(labeled_data):
    for row in tqdm(labeled_data, total=labeled_data.count, unit=' rows'):
        relevant_tags = preproc.extract_relevant_tags(row.html)
        vacancy_text = ' '.join((tag.getText() for tag in relevant_tags))
        words = preproc.remove_stop_words(vacancy_text)
        if len(words) > 0:
            yield words, row.title


max_features = 500
data_train = X28TrainData(args)
data_test = X28TestData(args)


def create_data_labels(dataset):
    data = []
    labels = []
    for raw_data, label in dataset:
        data.append(raw_data)
        labels.append(label)
    return data, labels


def load_data(name, dataset, transform_fun, file_features, file_labels):
    if args.rebuild or not os.path.isfile(file_features):
        log.info('loading/cleaning {} data from DB...'.format(name))
        data, labels = create_data_labels(dataset)
        log.info('created {} elements with {} labels'.format(len(data), len(labels)))

        log.info('creating features from {} data...'.format(name))
        features = transform_fun(data)
        features = features.toarray()

        log.info('saving {}x{} features to file'.format(features.shape[0], features.shape[1]))
        pickle.dump(labels, open(file_labels, 'wb'))
        pickle.dump(features, open(file_features, 'wb'))
        return features, labels
    else:
        log.info('Loading {} data and labels from file...'.format(name))
        data = pickle.load(open(file_features, 'rb'))
        labels = pickle.load(open(file_labels, 'rb'))
        return data, labels


def create_train_data(vectorizer):
    features, labels = load_data(name='train',
                                 dataset=preprocess(data_train),
                                 transform_fun=vectorizer.fit_transform,
                                 file_features=file_train_features,
                                 file_labels=file_train_labels
                                 )
    log.info('saving vectorizer to file')
    pickle.dump(vectorizer, open(file_vectorizer, 'wb'))
    return features, labels


def create_test_data(vectorizer):
    return load_data(name='test',
                     dataset=preprocess(data_test),
                     transform_fun=vectorizer.transform,
                     file_features=file_test_features,
                     file_labels=file_test_labels
                     )


def create_vectorizer(args):
    if args.rebuild or not os.path.isfile(file_vectorizer):
        log.info('recreating vectorizer...')
        return CountVectorizer(analyzer="word",
                               tokenizer=None,
                               preprocessor=None,
                               stop_words=None,
                               max_features=max_features
                               )
    else:
        log.info('loading vectorizer from file...')
        return pickle.load(open(file_vectorizer, 'rb'))


def train_random_forest():
    if os.path.exists(file_clf_random_forest):
        log.info('Loading RandomForestClassifier from file')
        return pickle.load(open(file_clf_random_forest, 'rb'))

    log.info('Training new RandomForestClassifier')
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(train_features, train_labels)
    pickle.dump(clf, open(file_clf_random_forest, 'wb'))
    return clf


if __name__ == '__main__':
    # create test/training data
    log.info('Creating training data')
    vectorizer = create_vectorizer(args)
    train_features, train_labels = create_train_data(vectorizer)

    # train classifier
    forest = train_random_forest()

    # make predictions
    test_features, test_labels = create_test_data(vectorizer)
    log.info('using trained RandomForestClassifier to predict test features')
    predictions = forest.predict(test_features)

    # evaluate_avg predictions
    log.info('measuring accuracy of predictions')
    e_strict = StrictJobtitleClassificationScorer()
    e_tolerant = TolerantJobtitleClassificationScorer()
    e_linear = LinearJobtitleClassificationScorer()
    acc_strict = e_strict.evaluate_all(test_labels, predictions)
    acc_tolerant = e_tolerant.evaluate_all(test_labels, predictions)
    acc_linear = e_linear.evaluate_all(test_labels, predictions)

    log.info('accuracy (strict): {}'.format("{:1.4f}".format(acc_strict)))
    log.info('accuracy (tolerant): {}'.format("{:1.4f}".format(acc_tolerant)))
    log.info('accuracy (linear): {}'.format("{:1.4f}".format(acc_linear)))
