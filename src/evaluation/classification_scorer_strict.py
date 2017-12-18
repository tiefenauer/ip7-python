from abc import abstractmethod

from src.evaluation.classification_scorer import ClassificationScorer


class StrictClassificationScorer(ClassificationScorer):

    def __init__(self):
        super(StrictClassificationScorer, self).__init__(label='strict')

    @abstractmethod
    def calculate_similarity(self, actual_class, predicted_class):
        """to bed implemented in subclass"""
        return 0
