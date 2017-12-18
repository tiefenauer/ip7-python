import logging
from abc import ABC, abstractmethod

from tqdm import tqdm

log = logging.getLogger(__name__)


class Preprocessor(ABC):

    def __init__(self, data_source=None):
        if data_source:
            self.raw_data = data_source
            self.count = len(data_source)
        else:
            self.raw_data = []
            self.count = 0

    def __iter__(self):
        for row in tqdm((row for row in self.raw_data if row.html), total=self.count):
            row_processed = self.preprocess_single(row)
            yield row, row_processed

    @abstractmethod
    def preprocess_single(self, row):
        """preprocess some HTML content and return the result in the desired format"""
