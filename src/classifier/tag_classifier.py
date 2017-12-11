from abc import abstractmethod

from src.classifier.classifier import Classifier
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor


class TagClassifier(Classifier):
    """An FTS classifier predicts the class by performing a full text search (FTS) on the processed data."""

    def __init__(self, args, preprocessor=RelevantTagsPreprocessor):
        super(TagClassifier, self).__init__(args, preprocessor)

    @abstractmethod
    def classify(self, processed_data):
        """to be implemented in subclass"""
        return

    def get_filename_postfix(self):
        return ''
