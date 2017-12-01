from abc import ABC, abstractmethod


class DataProcessor(ABC):
    """a data processor is something that finds information in data"""

    @abstractmethod
    def title(self):
        """a short title of the classification strategy"""
        return

    @abstractmethod
    def description(self):
        """describe how the classification is done"""
        return

    @abstractmethod
    def label(self):
        """short label for visualisation"""
        return
