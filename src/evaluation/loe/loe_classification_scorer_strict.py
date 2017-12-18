from src.evaluation.classification_scorer_strict import StrictClassificationScorer


class StrictLoeClassificationScorer(StrictClassificationScorer):
    def calculate_similarity(self, loe_actual, loe_predicted):
        return int(loe_actual == loe_predicted)
