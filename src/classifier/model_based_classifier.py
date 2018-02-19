import logging
import re
from abc import abstractmethod

from src.classifier.classifier import Classifier

log = logging.getLogger(__name__)

gzip_filename_pattern = re.compile('(\.gz)$')


class ModelClassifier(Classifier):
    """A ModelClassifier classifies some unknown, preprocessed data using a trained model. The training of the model
    must be done before classification. Alternatively, a pre-trained model can be loaded from file by supplying a
    filename as an argument (args.model). The file must exist in ./resource/models/. The pre-trained model will then be
    loaded upon instantiation.
    If no filename is supplied, the file does not exist or the model can not be loaded for any other reason, a new
    model will be trained. Training of a new model can take considerably more time than loading a pre-trained model!"""

    def __init__(self, model):
        super(ModelClassifier, self).__init__()
        self.model = model

    @abstractmethod
    def predict_class(self, processed_data):
        """get class for a single item of """
