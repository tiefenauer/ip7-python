from abc import abstractmethod

from src.scoring.scorer import Scorer


class LinearScorer(Scorer):

    def __init__(self):
        super(LinearScorer, self).__init__(label='linear')

    @abstractmethod
    def _calculate_similarity(self, actual_class, predicted_class):
        """to bed implemented in subclass"""
        return 0
