import logging
import os
import sys
from abc import ABC, abstractmethod

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

data_dir = 'D:/code/ip7-python/resource/models/word2vec'
if not os.path.isdir(data_dir):
    os.makedirs(data_dir)


class ClassificationStrategy(ABC):
    def __init__(self, model_file=None):
        self.model_file = model_file

    def train_model(self, data):
        if self.model_file:
            path = os.path.join(data_dir, self.model_file)
            model = self.load_model(path) if self.model_file else None
            if model:
                return model
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
        logging.info('load_model: Trying to load model from {}'.format(filename))
        model = self._load_model(filename)
        if model:
            logging.info('load_model: Successfully loaded model from {}'.format(filename))
        else:
            logging.info('load_model: Could not load model from {}'.format(filename))
        return model

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
