from abc import abstractmethod

from src.core.data_processor import DataProcessor


class Extractor(DataProcessor):
    def __init__(self, args, preprocesor):
        super(Extractor, self).__init__(args, preprocesor)
        self._process = self.extract

    @abstractmethod
    def extract(self, data):
        """extract the information from data"""
        return
