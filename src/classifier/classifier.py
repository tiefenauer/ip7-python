import os
import time
from abc import ABC, abstractmethod

from src.util import util

model_dir = 'D:/code/ip7-python/resource/models'


def path_to_file(filename):
    if not os.path.isdir(model_dir):
        os.makedirs(model_dir)
    return os.path.join(model_dir, filename)


class Classifier(ABC):
    """Abstract base class for a classifier. A classifier takes input data of any kind and converts it using a
    preprocessor. The converted format is used to make the classification."""

    def __init__(self, args, preprocessor):
        self.preprocessor = preprocessor
        self.filename = self.default_filename()

    def classify_all(self, raw_data):
        """Preprocess each item of an iterable set of raw data. The  by preprocessing it and forwarding the preprocessed data to the
        abstract method whose further logic depends on the implementing subclass"""
        processed_rows = self.preprocessor(raw_data)
        for row in processed_rows:
            rowid = row.id
            actual_class = self.get_actual_class(row)
            predicted_class = self.classify(row.processed)
            yield rowid, actual_class, predicted_class

    def default_filename(self):
        time_str = time.strftime(util.DATE_PATTERN)
        label = self.label()
        postfix = self.get_filename_postfix()
        filename = '{label}_{time}'.format(label=label, time=time_str)
        if postfix:
            filename += '_{postfix}'.format(postfix=postfix)
        return filename

    @abstractmethod
    def classify(self, preprocessed_data):
        """classify the peprocessed data of a single input row and return the predicted class"""
        return

    @abstractmethod
    def get_actual_class(self, row):
        """return the actual class for an input row"""
        return

    @abstractmethod
    def title(self):
        """a short title of the classifier to be used for display"""
        return

    @abstractmethod
    def label(self):
        """short label for visualisation"""
        return

    @abstractmethod
    def get_filename_postfix(self):
        """return a custom string to append to the default filename pattern"""
