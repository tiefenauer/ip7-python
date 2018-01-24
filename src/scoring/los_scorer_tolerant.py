from src.evaluation.classification_scorer_tolerant import TolerantClassificationScorer


class TolerantLoeScorer(TolerantClassificationScorer):

    def _calculate_similarity(self, actual_class, predicted_class):
        return 1 if any(t in predicted_class for t in actual_class) else 0
