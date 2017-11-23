import logging
from abc import ABC, abstractmethod

from tqdm import tqdm

log = logging.getLogger(__name__)


class X28Preprocessor(ABC):
    def preprocess(self, data, num_rows):
        log.info('Preprocessing X28 data...')
        for row in tqdm((row for row in data if row.html), total=num_rows):
            row.processed = self.preprocess_single(row)
            yield row

    @abstractmethod
    def preprocess_single(self, row):
        """preprocess some HTML content and return the result in the desired format"""
