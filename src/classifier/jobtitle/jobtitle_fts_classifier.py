import logging
from abc import abstractmethod

from src.classifier.fts_classifier import FtsClassifier
from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.preprocessing.fts_preprocessor import FtsPreprocessor

log = logging.getLogger(__name__)


class JobtitleFtsClassifier(FtsClassifier, JobtitleClassifier):

    def __init__(self, args):
        preprocessor = FtsPreprocessor()
        super(JobtitleFtsClassifier, self).__init__(args, preprocessor)

    @abstractmethod
    def title(self):
        """to be implemented in subclass"""

    @abstractmethod
    def description(self):
        """to be implemented in subclass"""

    @abstractmethod
    def label(self):
        """to be implemented in subclass"""

    def get_filename_postfix(self):
        return ''
