from abc import abstractmethod

from src.evaluation.classification_scorer import ClassificationScorer


class TolerantClassificationScorer(ClassificationScorer):

    def __init__(self):
        super(TolerantClassificationScorer, self).__init__(label='tolerant')

    @abstractmethod
    def calculate_similarity(self, actual_class, predicted_class):
        """to bed implemented in subclass"""
        return 0
