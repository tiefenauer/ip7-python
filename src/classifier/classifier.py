import gzip
import logging
import os
import shutil
import time
from abc import ABC, abstractmethod

from src.util import util

log = logging.getLogger(__name__)

data_dir = 'D:/code/ip7-python/resource/models'


class Classifier(ABC):
    def __init__(self, args, preprocessor):
        self.preprocessor = preprocessor
        model_file = args.model if hasattr(args, 'model') and args.model else None
        self.model = None
        if model_file:
            self.model = self.load_model(model_file)

    def train_model(self, train_data):
        if self.model:
            return self.model

        log.info('train_model: Training new model...')
        processed_data = (row.processed for row in self.preprocessor.preprocess(train_data, train_data.num_rows))
        labels = (row.title for row in train_data)
        self.model = self._train_model(processed_data, labels, train_data.num_rows)
        log.info('train_model: done!')
        #
        self.save_model()
        return self.model

    def save_model(self, filename=None):
        log.info('save_model: Saving model...')
        path = self.get_model_path(filename)
        # save
        self._save_model(self.model, path)
        # compress
        path_gz = path + '.gz'
        with open(path, 'rb') as f_in, gzip.open(path_gz, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(path)
        return path_gz

    def load_model(self, filename=None):
        path = self.get_model_path(filename)
        log.info('load_model: Trying to load model from {}'.format(path))
        model = self._load_model(path)
        if model:
            log.info('load_model: Successfully loaded model from {}'.format(path))
        else:
            log.info('load_model: Could not load model from {}'.format(path))
        return model

    def default_filename(self):
        time_str = time.strftime(util.DATE_PATTERN)
        label = self.label()
        postfix = self._get_filename_postfix()
        filename = '{label}_{time}'.format(label=label, time=time_str)
        if postfix:
            filename += '_{postfix}'.format(postfix=postfix)
        return filename

    def get_model_path(self, filename=None):
        if filename is None:
            filename = self.default_filename()
        path = os.path.join(data_dir, self.label())
        if not os.path.isdir(path):
            os.makedirs(path)
        return os.path.join(path, filename)

    @abstractmethod
    def _get_filename_postfix(self):
        """return a custom string to append to the default filename pattern"""

    @abstractmethod
    def _train_model(self, processed_data, labels, num_rows):
        """train classifier with some given data"""

    @abstractmethod
    def _save_model(self, model, path):
        """train classifier with some given data"""

    @abstractmethod
    def _load_model(self, path):
        """train classifier with some given data"""

    @abstractmethod
    def classify(self, processed_data):
        """classify some new data and return the class label"""

    @abstractmethod
    def title(self):
        """a short title of the classification strategy"""

    @abstractmethod
    def description(self):
        """describe how the classification is done"""

    @abstractmethod
    def label(self):
        """short label for visualisation"""
