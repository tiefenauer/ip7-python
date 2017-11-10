import logging
import sys
from abc import ABC, abstractmethod

from tqdm import tqdm

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Preprocessor(ABC):
    def __init__(self, data=None):
        self.data = data

    def __iter__(self):
        if not self.data:
            return
        for row in (row for row in tqdm(self.data, total=self.data.num_rows, unit=' rows') if row['html']):
            yield self.preprocess_single(row['html'])

    def preprocess(self, data):
        logging.info('Preprocessing data...')
        processed_data = []
        for row in (row for row in tqdm(data, total=data.num_rows, unit=' rows') if row['html']):
            processed_data += self.preprocess_single(row['html'])
        logging.info('...done! Got {} processed items'.format(len(processed_data)))
        return processed_data

    @abstractmethod
    def preprocess_single(self, markup):
        """preprocess some HTML content and return the result in the desired format"""
