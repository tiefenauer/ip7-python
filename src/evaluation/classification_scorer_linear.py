from abc import abstractmethod

from src.evaluation.classification_scorer import ClassificationScorer


class LinearClassificationScorer(ClassificationScorer):

    def __init__(self):
        super(LinearClassificationScorer, self).__init__(label='linear')

    @abstractmethod
    def calculate_similarity(self, actual_class, predicted_class):
        """to bed implemented in subclass"""
        return 0
