from src.evaluation.classification_scorer_strict import StrictClassificationScorer


class StrictJobtitleClassificationScorer(StrictClassificationScorer):

    def _calculate_similarity(self, actual_class, predicted_class):
        return int(actual_class == predicted_class)
