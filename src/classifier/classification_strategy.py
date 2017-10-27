from abc import ABC, abstractmethod


class ClassificationStrategy(ABC):
    @abstractmethod
    def classify(self, tags):
        """get a list of tags and predict the class"""

    @abstractmethod
    def title(self):
        """a short title of the classification strategy"""

    @abstractmethod
    def description(self):
        """describe how the classification is done"""
