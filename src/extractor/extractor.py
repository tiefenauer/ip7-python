from abc import abstractmethod

from src.core.data_processor import DataProcessor


class Extractor(DataProcessor):
    def __init__(self, args, preprocesor):
        self.preprocessor = preprocesor

    @abstractmethod
    def extract(self, data):
        """extract the information from data"""
        return
