from abc import abstractmethod

from src.classifier.classifier import Classifier


class JobtitleClassifier(Classifier):
    """Uses row.title attribute as the actual class"""

    @abstractmethod
    def classify(self, preprocessed_data):
        """to be implemented in subclass"""
        return

    def get_actual_class(self, row):
        return row.title
