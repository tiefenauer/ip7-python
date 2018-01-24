from src.scoring.scorer_linear import LinearScorer


class LinearLoeScorer(LinearScorer):
    scores = 0

    def _calculate_similarity(self, loe_actual, loe_predicted):
        actual_min, actual_max = loe_actual
        predicted_min, predicted_max = loe_predicted
        sum = 0
        sum += int(actual_min == predicted_min)
        sum += int(actual_max == predicted_max)
        return sum / len(loe_actual)
