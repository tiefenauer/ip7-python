import logging
from abc import abstractmethod

from src.classifier.core.fts_classifier import FtsClassifier

log = logging.getLogger(__name__)


class JobtitleFtsClassifier(FtsClassifier):

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
