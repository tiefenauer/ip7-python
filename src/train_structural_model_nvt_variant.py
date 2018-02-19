"""
Train a NaiveBayes classifier (NLTK-implementation) to use in the structural approach (NVT-Variant)
"""

import logging
import os
import pickle

import nltk

from src.classifier.jobtitle.jobtitle_classifier_structural_nvt import extract_features
from src.database.train_data_x28 import X28TrainData
from src.importer.known_jobs import KnownJobs
from src.preprocessing.structural_preprocessor_nvt import StructuralPreprocessorNVT
from src.util.globals import MODELS_DIR
from src.util.jobtitle_util import to_male_form
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

model_path = os.path.join(MODELS_DIR, 'structural_nvt.nb')
known_jobs = KnownJobs()


def train_naive_bayes(labeled_featuresets):
    """train a Naive Bayes classifier with given labeled data"""

    if os.path.exists(model_path):
        log.info('Loading Naive Bayes classifier from {}'.format(model_path))
        return pickle.load(open(model_path, 'rb'))

    log.info('training new Naive Bayes Classifier')
    clf = nltk.NaiveBayesClassifier.train(labeled_featuresets)
    with open(model_path, 'wb') as clf_file:
        log.info('saving trained classifier to {}'.format(model_path))
        pickle.dump(clf, clf_file)
    return clf


def find_job_name(x28_title):
    """search X28-Label for known job name"""
    for job_name_m in (to_male_form(job_name) for job_name in known_jobs):
        if job_name_m in x28_title:
            return job_name_m
    # no known job name found ==> return original X28-Title
    return x28_title


if __name__ == '__main__':
    preprocessed_data = StructuralPreprocessorNVT(X28TrainData())
    X = (extract_features(row_processed) for row, row_processed in preprocessed_data)
    y = (find_job_name(row.title) for row, row_processed in preprocessed_data)

    labeled_featuresets = zip(X, y)
    model = train_naive_bayes(labeled_featuresets)
