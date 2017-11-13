import logging
import os
import sys
from abc import ABC, abstractmethod

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

data_dir = 'D:/code/ip7-python/resource/models/word2vec'
if not os.path.isdir(data_dir):
    os.makedirs(data_dir)


class Classifier(ABC):
    def __init__(self, model_file=None):
        if model_file:
            self.model = self.load_model(model_file)
        else:
            self.model = None

    def train_model(self, data):
        if self.model:
            return self.model

        logging.info('train_model: Training new model...')
        model = self._train_model(data)
        logging.info('train_model: done!')
        self.save_model(model)
        return model

    def save_model(self, model, binary=True, zipped=True):
        logging.info('save_model: Saving model...')
        filename = self._save_model(model, binary, zipped)
        logging.info('save_model: done! Saved under ' + filename)
        return filename

    def load_model(self, filename):
        path = os.path.join(data_dir, filename)
        logging.info('load_model: Trying to load model from {}'.format(path))
        model = self._load_model(path)
        if model:
            logging.info('load_model: Successfully loaded model from {}'.format(path))
        else:
            logging.info('load_model: Could not load model from {}'.format(path))
        return model if model else None

    @abstractmethod
    def _train_model(self, data):
        """train classifier with some given data"""

    @abstractmethod
    def _save_model(self, model, binary, zipped):
        """train classifier with some given data"""

    @abstractmethod
    def _load_model(self, filename):
        """train classifier with some given data"""

    @abstractmethod
    def classify(self, data):
        """classify some new data and return the class label"""

    @abstractmethod
    def title(self):
        """a short title of the classification strategy"""

    @abstractmethod
    def description(self):
        """describe how the classification is done"""

    @abstractmethod
    def label(self):
        """short label for visualisation"""
