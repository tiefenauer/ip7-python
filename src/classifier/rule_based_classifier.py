from abc import abstractmethod

from src.classifier.classifier import Classifier


class RuleBasedClassifier(Classifier):
    """An FTS classifier predicts the class by performing a full text search (FTS) on the processed data."""

    @abstractmethod
    def predict_class(self, processed_data):
        """to be implemented in subclass"""
        return

    def get_filename_postfix(self):
        return ''
