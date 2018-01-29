import logging
import os
import pickle
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from tqdm import tqdm

from src.classifier.jobtitle.jobtitle_classifier_structural import extract_nouns_and_verbs_from_row
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
x28_corpus = 'x28.corpus'
tfidf_vectorizer = 'tfidf.vectorizer'
tfidf_vectors = 'tfidf.vectors'
multinomial_nb = 'multinomial.nb'
x28_corpus_path = resource_dir + x28_corpus
simplified_corpus_path = x28_corpus_path + '.simplified'
tfidf_vectorizer_path = resource_dir + tfidf_vectorizer
tfidf_vectors_path = resource_dir + tfidf_vectors
multinomial_nb_path = resource_dir + multinomial_nb

special_chars = re.compile('([^A-Za-zäöüéèà]*)')

structural_preprocessor = StructuralPreprocessor()
known_jobs = set(KnownJobs())


class X28Corpus(object):

    def __init__(self):
        self.plaintexts = []
        self.titles = []
        self.nouns = []
        self.verbs = []
        self.labels = []
        self.labels_simplified = []

    def add_sample(self, plaintext, title, nouns, verbs, label, label_simplified):
        self.plaintexts.append(plaintext)
        self.titles.append(title)
        self.nouns.append(nouns)
        self.verbs.append(verbs)
        self.labels.append(label)
        self.labels_simplified.append(label_simplified)


def extract_label(row):
    label = None
    label_simplified = None
    # search known job in label
    for job_name_m in (jnm for jnm in
                       (jobtitle_util.to_male_form(job_name) for job_name in (job_name for job_name in known_jobs)) if
                       jnm.lower() in row.title.lower()):
        p = re.compile(r'\b[^\s^\/]*{}[^\s^\/]*\b'.format(re.escape(job_name_m)), re.IGNORECASE)
        m = re.findall(p, row.title)
        if m:
            label_simplified = m[0]
            label = expand_left_right(label_simplified, row.title)
            break
    if not label_simplified:
        return None, None
    label = remove_percentage(label)
    label = remove_mw(label)
    label = ' '.join(word for word in label.split(' ') if not word.isupper())
    return label, label_simplified


def create_corpus():
    if os.path.exists(x28_corpus_path):
        log.info('loading corpus from {}'.format(x28_corpus_path))
        return pickle.load(open(x28_corpus_path, 'rb'))

    corpus = X28Corpus()
    log.info('Creating new corpus')
    for row in tqdm(X28Data()):
        label, label_simplified = extract_label(row)
        if not label_simplified:
            continue
        nouns, verbs = extract_nouns_and_verbs_from_row(row)
        corpus.add_sample(row.plaintext, row.title, nouns, verbs, label, label_simplified)

    with open(x28_corpus_path, 'wb') as corpusfile:
        log.info('Saving corpus to {}'.format(x28_corpus_path))
        pickle.dump(corpus, corpusfile)

    return corpus


def train_vectorizer(docs, min_df=1):
    if os.path.exists(tfidf_vectors_path):
        log.info('loading fitted vectors from {}'.format(tfidf_vectors_path))
        return pickle.load(open(tfidf_vectors_path, 'rb'))

    log.info('Training new TfidfVectorizer')
    tfidf_vect = TfidfVectorizer(min_df=min_df)
    X = tfidf_vect.fit_transform(docs)
    log.info('Trained TfIdfVectorizer: {} words. '.format(X.shape))
    with open(tfidf_vectorizer_path, 'wb') as vectorizer_file, open(tfidf_vectors_path, 'wb') as vectors_file:
        log.info('saving vectorizer to {}'.format(tfidf_vectorizer_path))
        pickle.dump(tfidf_vect, vectorizer_file)
        log.info('saving fitted vectors to {}'.format(tfidf_vectors_path))
        pickle.dump(X, vectors_file)
    return X


def train_classifier(X, y, min_df=1):
    log.info('Training Classifier')
    clf = MultinomialNB()
    clf.fit(X, y)
    with open(multinomial_nb_path, 'wb') as clf_file:
        log.info('saving trained classifier to {}'.format(multinomial_nb_path))
        pickle.dump(clf, clf_file)
    return clf


if __name__ == '__main__':
    # corpus_new = X28Corpus()
    # with open(x28_corpus_path, 'rb') as corpus_read:
    #     corpus = pickle.load(corpus_read)
    #     rows = list(zip(corpus.titles, corpus.plaintexts, corpus.labels, corpus.labels_simplified))
    #     for title, plaintext, label, label_simplified in tqdm(rows):
    #         row = create_dummy_row(title=title, plaintext=plaintext)
    #         nouns, verbs = extract_nouns_and_verbs(row)
    #         corpus_new.add_sample(row.plaintext, row.title, nouns, verbs, label, label_simplified)
    #
    # with open(x28_corpus_path, 'wb') as corpus_write:
    #     pickle.dump(corpus_new, corpus_write)
    corpus = create_corpus()
    log.info('corpus.data={}, corpus.target={}'.format(len(corpus.nouns), len(corpus.labels)))
    # docs = list(nouns + ' ' + verbs for (nouns, verbs) in zip(corpus.nouns, corpus.verbs))
    docs = corpus.plaintexts
    X = train_vectorizer(docs, 10)
    y = corpus.labels_simplified
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    clf = train_classifier(X_train, y_train)
    predicted = clf.predict(X_test)
    mean = np.mean(predicted == y_test)
    log.info('mean accuracy: {}'.format(mean))
