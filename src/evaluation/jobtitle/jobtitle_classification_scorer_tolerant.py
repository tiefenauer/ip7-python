from src.evaluation.classification_scorer_tolerant import TolerantClassificationScorer
from src.util import jobtitle_util


class TolerantJobtitleClassificationScorer(TolerantClassificationScorer):
    """assigns a score of 1 if predicted class appears at least once in actual class
    predicted and actual class are normalized in order to compare them.
    """

    def calculate_similarity(self, actual_class, predicted_class):
        similarity = 0
        # normalize before comparison
        actual_class_normalized = jobtitle_util.normalize_job_title(actual_class)
        predicted_class_normalized = jobtitle_util.normalize_job_name(predicted_class)

        if predicted_class and predicted_class_normalized in actual_class_normalized:
            similarity = 1
        return similarity
