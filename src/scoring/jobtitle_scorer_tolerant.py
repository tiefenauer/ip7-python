from src.scoring.scorer_tolerant import TolerantScorer
from src.util import jobtitle_util


class TolerantJobtitleScorer(TolerantScorer):
    """assigns a score of 1 if predicted class appears at least once in actual class
    predicted and actual class are normalized in order to compare them.
    """

    def _calculate_similarity(self, actual_class, predicted_class):
        if not predicted_class:
            return 0
        # normalize before comparison
        actual_class_normalized = ' '.join(jobtitle_util.normalize_job_title(actual_class))
        predicted_class_normalized = ' '.join(jobtitle_util.normalize_job_title(predicted_class))

        if predicted_class_normalized in actual_class_normalized:
            return 1
        return 0
