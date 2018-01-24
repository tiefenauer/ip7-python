from src.evaluation.classification_scorer_strict import StrictClassificationScorer


class StrictJobtitleScorer(StrictClassificationScorer):

    def _calculate_similarity(self, actual_class, predicted_class):
        return int(actual_class == predicted_class)
