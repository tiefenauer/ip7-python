import logging
from abc import abstractmethod

from src.extractor.extractor import Extractor

log = logging.getLogger(__name__)


class JobtitleExtractor(Extractor):

    @abstractmethod
    def title(self):
        """to be implemented in subclass"""

    @abstractmethod
    def description(self):
        """to be implemented in subclass"""

    @abstractmethod
    def label(self):
        """to be implemented in subclass"""

    def _get_filename_postfix(self):
        return ''
