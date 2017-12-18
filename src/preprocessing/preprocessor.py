import logging
from abc import ABC, abstractmethod

from tqdm import tqdm

log = logging.getLogger(__name__)


class Preprocessor(ABC):

    def __init__(self, data_source=None):
        self.raw_data = data_source if data_source else []

    def __iter__(self):
        for row in tqdm(self.raw_data, unit=' rows'):
            yield row, self.preprocess_single(row)

    def __len__(self):
        return len(self.raw_data)

    @abstractmethod
    def preprocess_single(self, row):
        """preprocess some HTML content and return the result in the desired format"""
