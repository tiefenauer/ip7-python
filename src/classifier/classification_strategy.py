from abc import ABC, abstractmethod


class ClassificationStrategy(ABC):
    @abstractmethod
    def train(self, data):
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
