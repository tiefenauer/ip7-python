import os
import time
from abc import ABC, abstractmethod

from src.util import util

data_dir = 'D:/code/ip7-python/resource/models'


def path_to_file(filename):
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, filename)


class Classifier(ABC):
    """a data processor is something that finds information in data"""

    def __init__(self, args, preprocessor):
        self.preprocessor = preprocessor
        self.filename = self.default_filename()

    def classify_all(self, raw_data):
        """process an iterable set of raw data by preprocessing it and forwarding the preprocessed data to the
        abstract method whose further logic depends on the implementing subclass"""
        num_rows = raw_data.num_rows if hasattr(raw_data, 'num_rows') else -1
        rows_preprocessed = self.preprocessor.preprocess(raw_data, num_rows)
        for row in rows_preprocessed:
            row.predicted_class = self.classify(row)
            yield row

    def default_filename(self):
        time_str = time.strftime(util.DATE_PATTERN)
        label = self.label()
        postfix = self.get_filename_postfix()
        filename = '{label}_{time}'.format(label=label, time=time_str)
        if postfix:
            filename += '_{postfix}'.format(postfix=postfix)
        return filename

    @abstractmethod
    def classify(self, row_preprocessed):
        """process single preprocessed row returning the result for each item"""
        return

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

    @abstractmethod
    def get_filename_postfix(self):
        """return a custom string to append to the default filename pattern"""
