import gzip
import pickle
from abc import abstractmethod

import nltk

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.model_classifier import ModelClassifier
from src.dataimport.known_jobs import KnownJobs
from src.util import jobtitle_util


def clean_labels(labels_list):
    known_jobs = KnownJobs()
    for label in labels_list:
        # search known job in label
        for job_name_m in (jobtitle_util.to_male_form(job_name) for job_name in known_jobs):
            if job_name_m in label:
                yield job_name_m
        # known job not found ==> return original label
        yield label


class JobtitleStructuralClassifier(ModelClassifier, JobtitleClassifier):
    """Classifier to predict job title using structural information from preprocessed data. Structural data usually
    consists of the tokenized words and some additional information about the inner structure of the text.
    A Naive Bayes classifier is trained to make predictions about the job title for unkown instances.
    """

    def __init__(self, args, preprocessor):
        self.num_rows = 0
        super(JobtitleStructuralClassifier, self).__init__(args, preprocessor)

    def classify(self, tagged_word_tokens):
        features = self.extract_features(tagged_word_tokens)
        result = self.model.classify(features)
        return result

    def train_model(self, data_train):
        """Train a Naive Bayes classifier as the internal model"""
        self.num_rows = data_train.num_rows
        processed_data = self.preprocessor(data_train)
        data = (row.processed for row in processed_data)
        labels = clean_labels(row.title for row in processed_data)
        labeled_data = zip(data, labels)
        train_set = ((self.extract_features(words), label) for words, label in labeled_data)
        model = nltk.NaiveBayesClassifier.train(train_set)
        return model

    def get_filename_postfix(self):
        return '{}rows'.format(self.num_rows)

    def serialize_model(self, model, path):
        with open(path, 'wb') as f:
            pickle.dump(model, f)
        return path

    def deserialize_model(self, path):
        model = None
        with gzip.open(path, 'rb') as f:
            model = pickle.load(f)
        return model

    @abstractmethod
    def extract_features(self, tagged_words):
        """extract features to be used to train the Naive Bayes classifier"""
