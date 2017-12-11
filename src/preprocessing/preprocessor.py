import logging
from abc import ABC, abstractmethod

from tqdm import tqdm

log = logging.getLogger(__name__)


class Preprocessor(ABC):

    def __init__(self, raw_data):
        self.raw_data = raw_data

    def __iter__(self):
        for row in tqdm((row for row in self.raw_data if row.html), total=self.raw_data.num_rows):
            row.processed = self.preprocess_single(row)
            yield row

    @abstractmethod
    def preprocess_single(self, row):
        """preprocess some HTML content and return the result in the desired format"""
