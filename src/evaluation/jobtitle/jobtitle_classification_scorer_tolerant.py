from src.evaluation.classification_scorer import ClassificationScorer
from src.util import jobtitle_util


class TolerantJobtitleClassificationScorer(ClassificationScorer):
    """assigns a score of 1 if predicted class appears at least once in actual class
    predicted and actual class are normalized in order to compare them.
    """

    def __init__(self):
        super(TolerantJobtitleClassificationScorer, self).__init__(label='tolerant')

    def calculate_similarity(self, actual_class, predicted_class):
        similarity = 0
        # normalize before comparison
        actual_class_normalized = jobtitle_util.normalize_text(actual_class)
        predicted_class_normalized = jobtitle_util.normalize_job_name(predicted_class)

        if predicted_class and predicted_class_normalized in actual_class_normalized:
            similarity = 1
        return similarity

    def label(self):
        return "tolerant"
