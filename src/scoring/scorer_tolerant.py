from abc import abstractmethod

from src.scoring.scorer import Scorer


class TolerantScorer(Scorer):

    def __init__(self):
        super(TolerantScorer, self).__init__(label='tolerant')

    @abstractmethod
    def _calculate_similarity(self, actual_class, predicted_class):
        """to bed implemented in subclass"""
        return 0
