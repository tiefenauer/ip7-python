import logging
import os
import pickle
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from tqdm import tqdm

from src.classifier.jobtitle.jobtitle_classifier_structural import extract_nouns
from src.database.x28_data import X28Data
from src.importer.known_jobs import KnownJobs
from src.preprocessing.structural_preprocessor import StructuralPreprocessor
from src.util import jobtitle_util
from src.util.jobtitle_util import remove_mw
from src.util.loe_util import remove_percentage
from src.util.log_util import log_setup
from src.util.pos_util import expand_left_right

log_setup()
log = logging.getLogger(__name__)

resource_dir = 'D:/code/ip7-python/resource/'
noun_corpus = 'noun.corpus'
tfidf_vectorizer = 'tfidf.vectorizer'
tfidf_vectors = 'tfidf.vectors'
multinomial_nb = 'multinomial.nb'
noun_corpus_path = resource_dir + noun_corpus
simplified_corpus_path = noun_corpus_path + '.simplified'
tfidf_vectorizer_path = resource_dir + tfidf_vectorizer
tfidf_vectors_path = resource_dir + tfidf_vectors
multinomial_nb_path = resource_dir + multinomial_nb

special_chars = re.compile('([^A-Za-zäöüéèà]*)')

structural_preprocessor = StructuralPreprocessor()
known_jobs = KnownJobs()


class NounCorpus(object):

    def __init__(self):
        self.data = []
        self.target = []

    def add_sample(self, data, target):
        self.data.append(data)
        self.target.append(target)


def extract_label(row, simplified):
    label = row.title
    # search known job in label
    for job_name_m in (jobtitle_util.to_male_form(job_name) for job_name in known_jobs):
        if job_name_m in row.title:
            label = job_name_m if simplified else expand_left_right(job_name_m, row.title)
            break
    label = remove_percentage(label)
    label = remove_mw(label)
    label = ' '.join(word for word in label.split(' ') if not word.isupper())
    return label


def create_corpus(path=noun_corpus_path, simplified=False, limit=0):
    if os.path.exists(path):
        log.info('loading corpus from {}'.format(path))
        return pickle.load(open(path, 'rb'))

    log.info('creating new corpus from {} rows'.format(limit))
    corpus = NounCorpus()
    i = 0
    for row in tqdm(X28Data()):
        tagged_words = structural_preprocessor.preprocess_single(row)
        data = extract_nouns(tagged_words)
        target = extract_label(row, simplified)
        corpus.add_sample(data, target)
        i += 1
        if i == limit:
            break
    with open(path, 'wb') as corpusfile:
        log.info('saving corpus to {}'.format(path))
        pickle.dump(corpus, corpusfile)

    return corpus


def train_vectorizer(corpus, min_df=1):
    log.info('Training TF/IDF Vectorizer')
    vectorizer = TfidfVectorizer(min_df=min_df)
    X = vectorizer.fit_transform(corpus.data)
    log.info('trained vectorizer: {} words. '.format(X.shape))
    with open(tfidf_vectorizer_path, 'wb') as vectorizer_file, open(tfidf_vectors_path, 'wb') as vectors_file:
        log.info('saving vectorizer to {}'.format(tfidf_vectorizer_path))
        pickle.dump(vectorizer, vectorizer_file)
        log.info('saving fitted vectors to {}'.format(tfidf_vectors_path))
        pickle.dump(X, vectors_file)
    return X


def train_classifier(X, y):
    log.info('Training MultinomialNB')
    clf = MultinomialNB().fit(X, y)
    with open(multinomial_nb_path, 'wb') as clf_file:
        log.info('saving trained classifier to {}'.format(multinomial_nb_path))
        pickle.dump(clf, clf_file)
    return clf


if __name__ == '__main__':
    X = train_vectorizer()
    y = np.array(corpus.target)
    log.info('X.shape={}, y.shape={}'.format(X.shape, y.shape))
    clf = train_classifier(X, y)
