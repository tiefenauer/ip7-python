import gzip
import logging
import os
import re
import shutil
from abc import abstractmethod

from src.classifier.core.classifier import Classifier

log = logging.getLogger(__name__)


class ModelClassifier(Classifier):
    def __init__(self, args, preprocessor):
        super(ModelClassifier, self).__init__(args, preprocessor)
        self.model = None

        # try to load model from model file (if specified)
        model_file = args.model if hasattr(args, 'model') and args.model else None
        if model_file:
            self.model = self.load_model(model_file)
            # adjust model filename
            self.model_file = self.get_model_path(re.sub('(\.gz)$', '', model_file))

    def _process(self, row_preprocessed):
        row_preprocessed.predicted_class = self.classify(row_preprocessed.processed)
        return row_preprocessed

    @abstractmethod
    def classify(self, processed_row):
        """classify some new data and return the class label"""

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
        self.model_file = path
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

    @abstractmethod
    def _train_model(self, processed_data, labels, num_rows):
        """train classifier with some given data"""
        return

    @abstractmethod
    def _save_model(self, model, path):
        """train classifier with some given data"""
        return

    @abstractmethod
    def _load_model(self, path):
        """train classifier with some given data"""
        return
