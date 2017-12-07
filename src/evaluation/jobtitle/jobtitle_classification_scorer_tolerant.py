from src.evaluation.classification_scorer import ClassificationScorer
from src.util import jobtitle_util


class TolerantJobtitleClassificationScorer(ClassificationScorer):

    def calculate_similarity(self, actual_class, predicted_class):
        similarity = 0
        if predicted_class and jobtitle_util.to_male_form(predicted_class) in actual_class:
            similarity = 1
        return similarity

    def label(self):
        return "tolerant"
