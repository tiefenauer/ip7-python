from abc import abstractmethod

from src.classifier.classifier import Classifier


class FtsClassifier(Classifier):

    def classify(self, processed_data):
        predicted_class = self.extract(processed_data)
        return predicted_class

    @abstractmethod
    def extract(self, processed_row):
        """extract the information from data"""
        return

    def get_filename_postfix(self):
        return ''
