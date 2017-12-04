import gzip
import logging
import os
import re
import shutil
from abc import abstractmethod

from src.classifier.classifier import Classifier, path_to_file

log = logging.getLogger(__name__)

gzip_filename_pattern = re.compile('(\.gz)$')


class ModelClassifier(Classifier):
    """A ModelClassifier classifies some unknown, preprocessed data using a trained model. The training of the model
    must be done before classification. Alternatively, a pre-trained model can be loaded from file by supplying a
    filename as an argument (args.model). The file must exist in ./resource/models/. The pre-trained model will then be
    loaded upon instantiation.
    If no filename is supplied, the file does not exist or the model can not be loaded for any other reason, a new
    model will be trained. Training of a new model can take considerably more time than loading a pre-trained model!"""

    def __init__(self, args, preprocessor):
        super(ModelClassifier, self).__init__(args, preprocessor)
        self.model = None

        # try to load model from model file (if specified)
        model_file = args.model if hasattr(args, 'model') and args.model else None
        if model_file:
            self.filename = model_file
            self.model = self.load_model()
            self.filename = re.sub(gzip_filename_pattern, '', model_file)

    def train_classifier(self, train_data):
        """train classifier by training the internal model saving it to file"""
        if self.model:
            log.info('Model present: using existing model')
            return self.model

        log.info('No model present: Training new model...')
        processed_data = (row.processed for row in self.preprocessor.preprocess(train_data, train_data.num_rows))
        labels = (row.title for row in train_data)
        self.model = self.train_model(processed_data, labels, train_data.num_rows)
        log.info('...done!')
        #
        self.save_model()
        return self.model

    def save_model(self):
        """compress and save a trained model to file"""
        path = path_to_file(self.filename)
        log.info('save_model: Saving model to {}'.format(path))
        # save
        self.serialize_model(self.model, path)
        # compress
        path_gz = path + '.gz'
        with open(path, 'rb') as f_in, gzip.open(path_gz, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(path)
        return path_gz

    def load_model(self):
        """load model from file"""
        path = path_to_file(self.filename)
        log.info('load_model: Trying to load model from {}'.format(path))
        model = self.deserialize_model(path)
        if model:
            log.info('load_model: Successfully loaded model from {}'.format(path))
        else:
            log.info('load_model: Could not load model from {}'.format(path))
        return model

    @abstractmethod
    def classify(self, processed_data):
        """get class for a single item of """

    @abstractmethod
    def train_model(self, processed_data, labels, num_rows):
        """train classifier with some given data"""
        return

    @abstractmethod
    def serialize_model(self, model, path):
        """save model to file using a suitable serialization strategy"""
        return

    @abstractmethod
    def deserialize_model(self, path):
        """load model from file using a suitable deserialization strategy"""
        return
