import gzip
import pickle
from abc import abstractmethod

import nltk

from src.classifier.model_classifier import ModelClassifier
from src.dataimport.known_jobs_tsv_importer import KnownJobsImporter
from src.util import jobtitle_util


def clean_labels(labels_list):
    known_jobs = KnownJobsImporter()
    for label in labels_list:
        # search known job in label
        for job_name_m in (jobtitle_util.to_male_form(job_name) for job_name in known_jobs):
            if job_name_m in label:
                yield job_name_m
        # known job not found ==> return original label
        yield label


class StructuralClassifier(ModelClassifier):
    def __init__(self, args, preprocessor):
        self.num_rows = 0
        super(StructuralClassifier, self).__init__(args, preprocessor)

    def classify(self, processed_row):
        features = self.extract_features(processed_row.processed)
        result = self.model.classify(features)
        return result

    def _train_model(self, processed_data, labels, num_rows):
        self.num_rows = num_rows
        cleaned_labels = clean_labels(labels)
        labeled_data = zip(processed_data, cleaned_labels)
        train_set = ((self.extract_features(words), label) for words, label in labeled_data)
        model = nltk.NaiveBayesClassifier.train(train_set)
        return model

    def get_filename_postfix(self):
        return '{}rows'.format(self.num_rows)

    def _save_model(self, model, path):
        with open(path, 'wb') as f:
            pickle.dump(model, f)
        return path

    def _load_model(self, path):
        model = None
        with gzip.open(path, 'rb') as f:
            model = pickle.load(f)
        return model

    @abstractmethod
    def extract_features(self, tagged_words):
        """to be implemented in subclass"""

    @abstractmethod
    def description(self):
        """to be implemented in subclass"""

    @abstractmethod
    def title(self):
        """to be implemented in subclass"""

    @abstractmethod
    def label(self):
        """to be implemented in subclass"""
