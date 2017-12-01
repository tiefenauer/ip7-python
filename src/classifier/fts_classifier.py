from abc import abstractmethod

from src.classifier.classifier import Classifier


class FtsClassifier(Classifier):

    def _process(self, row_preprocessed):
        row_preprocessed.predicted_class = self.extract(row_preprocessed.processed)
        return row_preprocessed

    @abstractmethod
    def extract(self, processed_row):
        """extract the information from data"""
        return

    def get_filename_postfix(self):
        return ''
