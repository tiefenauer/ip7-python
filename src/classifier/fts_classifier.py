import logging
from abc import abstractmethod

from src.classifier.classifier import Classifier

log = logging.getLogger(__name__)


class FtsClassifier(Classifier):
    def __init__(self, args, preprocessor):
        super(FtsClassifier, self).__init__(args, preprocessor)

    def _train_model(self, processed_data, labels, num_rows):
        log.info("no model to train in FTS")
        return None

    def _load_model(self, path):
        log.info("no model to load in FTS")
        return None

    def _save_model(self, path, binary, zipped):
        log.info("no model to save in FTS")
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
    def classify(self, processed_data):
        """to be implemented in subclass"""
