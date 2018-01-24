from src.scoring.scorer_strict import StrictScorer


class StrictJobtitleScorer(StrictScorer):

    def _calculate_similarity(self, actual_class, predicted_class):
        return int(actual_class == predicted_class)
