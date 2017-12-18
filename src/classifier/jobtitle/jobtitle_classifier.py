from abc import abstractmethod

from src.classifier.classifier import Classifier


class JobtitleClassifier(Classifier):
    """Uses row.title attribute as the actual class"""

    @abstractmethod
    def predict_class(self, processed_data):
        """to be implemented in subclass"""
        return

    def get_actual_class(self, row):
        return row.title
