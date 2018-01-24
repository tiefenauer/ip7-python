from src.scoring.scorer_strict import StrictScorer


class StrictLoeScorer(StrictScorer):
    def _calculate_similarity(self, loe_actual, loe_predicted):
        return int(loe_actual == loe_predicted)
