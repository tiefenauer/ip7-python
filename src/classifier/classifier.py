import os
from abc import ABC, abstractmethod

from src.util.globals import MODELS_DIR


def path_to_file(filename):
    if not os.path.isdir(MODELS_DIR):
        os.makedirs(MODELS_DIR)
    return os.path.join(MODELS_DIR, filename)


class Classifier(ABC):
    """Abstract base class for a classifier. A classifier takes input data of any kind and converts it using a
    preprocessor. The converted format is used to make the classification."""

    def classify(self, processed_data):
        """Preprocess each item of an iterable set of raw data. The  by preprocessing it and forwarding the preprocessed data to the
        abstract method whose further logic depends on the implementing subclass"""
        for row, row_processed in processed_data:
            actual_class = self.get_actual_class(row)
            predicted_class = self.predict_class(row_processed)
            yield row, actual_class, predicted_class

    @abstractmethod
    def predict_class(self, processed_data):
        """classify the peprocessed data of a single input row and return the predicted class"""
        return

    @abstractmethod
    def get_actual_class(self, row):
        """return the actual class for an input row"""
        return

    @abstractmethod
    def title(self):
        """a short title of the classifier to be used for display"""
        return

    @abstractmethod
    def label(self):
        """short label for visualisation"""
        return
