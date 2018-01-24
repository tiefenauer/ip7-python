from abc import abstractmethod

from src.scoring.scorer import Scorer


class StrictScorer(Scorer):

    def __init__(self):
        super(StrictScorer, self).__init__(label='strict')

    @abstractmethod
    def _calculate_similarity(self, actual_class, predicted_class):
        """to bed implemented in subclass"""
        return 0
