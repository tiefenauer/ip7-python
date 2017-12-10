from abc import abstractmethod

from src.classifier.classifier import Classifier
from src.preprocessing.fts_preprocessor import FtsPreprocessor


class FtsClassifier(Classifier):
    """An FTS classifier predicts the class by performing a full text search (FTS) on the processed data."""

    def __init__(self, args, preprocessor=FtsPreprocessor()):
        super(FtsClassifier, self).__init__(args, preprocessor)

    @abstractmethod
    def classify(self, processed_data):
        """to be implemented in subclass"""
        return

    def get_filename_postfix(self):
        return ''
