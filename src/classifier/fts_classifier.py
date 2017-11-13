import logging
import sys
from abc import abstractmethod

from src.classifier.classifier import Classifier

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class FullTextSearchClassifier(Classifier):
    def _train_model(self, data):
        logging.info("no model to train in FTS")
        return None

    def _load_model(self, filename):
        logging.info("no model to load in FTS")
        return None

    def _save_model(self, model, binary, zipped):
        logging.info("no model to save in FTS")
        return None

    @abstractmethod
    def title(self):
        """to be implemented in subclass"""

    @abstractmethod
    def description(self):
        """to be implemented in subclass"""

    @abstractmethod
    def label(self):
        """to be implemented in subclass"""

    @abstractmethod
    def classify(self, data):
        """to be implemented in subclass"""
