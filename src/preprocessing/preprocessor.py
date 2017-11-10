import logging
import sys
from abc import ABC, abstractmethod

from tqdm import tqdm

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Preprocessor(ABC):
    def __iter__(self):
        for row in (row for row in tqdm(self.data, total=self.data.num_rows, unit=' rows') if row['html']):
            yield self.preprocess_single(row['html'])

    def preprocess(self, data):
        logging.info('Preprocessing data...')
        self.data = data
        return self

    @abstractmethod
    def preprocess_single(self, markup):
        """preprocess some HTML content and return the result in the desired format"""
