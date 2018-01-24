from src.evaluation.classification_scorer_strict import StrictClassificationScorer


class StrictLoeScorer(StrictClassificationScorer):
    def _calculate_similarity(self, loe_actual, loe_predicted):
        return int(loe_actual == loe_predicted)
