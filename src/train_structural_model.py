"""
Train a Multinomial-NaiveBayes classifier (sklearn-implementation) to use in the structural approach (NVT-Variant)
"""

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
from src.scoring.jobtitle_scorer_linear import LinearJobtitleScorer
from src.scoring.jobtitle_scorer_strict import StrictJobtitleScorer
from src.scoring.jobtitle_scorer_tolerant import TolerantJobtitleScorer
from src.corpus.x28_corpus import X28Corpus
from src.util import jobtitle_util
from src.util.globals import MODELS_DIR, CORPUS_DIR
from src.util.jobtitle_util import remove_mw
from src.util.loe_util import remove_percentage
from src.util.log_util import log_setup
from src.util.pos_util import expand_left_right

log_setup()
log = logging.getLogger(__name__)

x28_corpus = os.path.join(CORPUS_DIR, 'x28.corpus')
x28_corpus_simplified = os.path.join(CORPUS_DIR, 'x28.corpus.simplified')
tfidf_vectorizer = os.path.join(MODELS_DIR, 'tfidf.vectorizer')
tfidf_vectors = os.path.join(MODELS_DIR, 'tfidf.vectors')
multinomial_nb = os.path.join(MODELS_DIR, 'multinomial.nb')

special_chars = re.compile('([^A-Za-zäöüéèà]*)')

structural_preprocessor = StructuralPreprocessor()
known_jobs = set(KnownJobs())


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
    if os.path.exists(x28_corpus):
        log.info('loading corpus from {}'.format(x28_corpus))
        return pickle.load(open(x28_corpus, 'rb'))

    corpus = X28Corpus()
    log.info('Creating new X28-corpus')
    for row in tqdm(X28Data()):
        label, label_simplified = extract_label(row)
        if not label_simplified:
            continue
        nouns, verbs = extract_nouns_and_verbs_from_row(row)
        corpus.add_sample(row.plaintext, row.title, nouns, verbs, label, label_simplified)

    with open(x28_corpus, 'wb') as corpusfile:
        log.info('Saving corpus to {}'.format(x28_corpus))
        pickle.dump(corpus, corpusfile)

    return corpus


def train_vectorizer(docs, min_df=1):
    if os.path.exists(tfidf_vectors):
        log.info('loading fitted vectors from {}'.format(tfidf_vectors))
        return pickle.load(open(tfidf_vectors, 'rb'))

    log.info('Training new TfidfVectorizer')
    tfidf_vect = TfidfVectorizer(min_df=min_df)
    X = tfidf_vect.fit_transform(tqdm(docs))
    log.info('Trained TfIdfVectorizer: {} words. '.format(X.shape))
    with open(tfidf_vectorizer, 'wb') as vectorizer_file, open(tfidf_vectors, 'wb') as vectors_file:
        log.info('saving vectorizer to {}'.format(tfidf_vectorizer))
        pickle.dump(tfidf_vect, vectorizer_file)
        log.info('saving fitted vectors to {}'.format(tfidf_vectors))
        pickle.dump(X, vectors_file)
    return X


def train_classifier(X, y):
    if os.path.exists(multinomial_nb):
        log.info('loading classifier from {}'.format(multinomial_nb))
        return pickle.load(open(multinomial_nb, 'rb'))

    log.info('Training new classifier')
    clf = MultinomialNB()
    clf.fit(X, y)
    with open(multinomial_nb, 'wb') as clf_file:
        log.info('saving trained classifier to {}'.format(multinomial_nb))
        pickle.dump(clf, clf_file)
    return clf


if __name__ == '__main__':
    # create corpus
    corpus = create_corpus()
    log.info('corpus.data={}, corpus.target={}'.format(len(corpus.nouns), len(corpus.labels)))

    # vectorize corpus
    # docs = list(nouns + ' ' + verbs for (nouns, verbs) in zip(corpus.nouns, corpus.verbs))
    docs = corpus.plaintexts
    X = train_vectorizer(docs, 10)
    y = corpus.labels_simplified
    y2 = corpus.labels

    # train classifier
    X_train, X_test, y_train, y_test, y2_train, y2_test = train_test_split(X, y, y2)
    clf = train_classifier(X_train, y_train)
    predictions = clf.predict(X_test)

    # evaluate classifier
    mean = np.mean(predictions == y_test)
    log.info('mean accuracy: {}'.format(mean))

    # evaluate with strict-, linear- and tolerant-score
    scorer_strict = StrictJobtitleScorer()
    scorer_linear = LinearJobtitleScorer()
    scorer_tolerant = TolerantJobtitleScorer()
    scores_strict = []
    scores_linear = []
    scores_tolerant = []
    log.info("Comparing with simplified label")
    for prediction, actual in tqdm(zip(predictions, y_test), total=len(predictions)):
        score_strict = scorer_strict.calculate_score(actual, prediction)
        score_linear = scorer_linear.calculate_score(actual, prediction)
        score_tolerant = scorer_tolerant.calculate_score(actual, prediction)
        scores_strict.append(score_strict)
        scores_linear.append(score_linear)
        scores_tolerant.append(score_tolerant)

    mean = np.mean(scores_strict)
    log.info('mean scores_strict: {}'.format(mean))
    mean = np.mean(scores_linear)
    log.info('mean scores_linear: {}'.format(mean))
    mean = np.mean(scores_tolerant)
    log.info('mean scores_tolerant: {}'.format(mean))

    log.info("Comparing with original label")
    for prediction, actual in tqdm(zip(predictions, y2_test), total=len(predictions)):
        score_strict = scorer_strict.calculate_score(actual, prediction)
        score_linear = scorer_linear.calculate_score(actual, prediction)
        score_tolerant = scorer_tolerant.calculate_score(actual, prediction)
        scores_strict.append(score_strict)
        scores_linear.append(score_linear)
        scores_tolerant.append(score_tolerant)
    mean = np.mean(scores_strict)
    log.info('mean scores_strict: {}'.format(mean))
    mean = np.mean(scores_linear)
    log.info('mean scores_linear: {}'.format(mean))
    mean = np.mean(scores_tolerant)
    log.info('mean scores_tolerant: {}'.format(mean))
