import logging
import sys
from abc import ABC, abstractmethod

from tqdm import tqdm

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class X28Preprocessor(ABC):
    def preprocess(self, data):
        logging.info('Preprocessing X28 data...')
        for row in (row for row in tqdm(data, total=data.num_rows, unit=' rows') if row['html']):
            row_id = row['id']
            target_class = row['title']
            processed_row = self.preprocess_single(row['html'])
            yield (row_id, target_class, processed_row)

    @abstractmethod
    def preprocess_single(self, markup):
        """preprocess some HTML content and return the result in the desired format"""
