from src.evaluation.classification_scorer import ClassificationScorer


class TolerantJobtitleClassificationScorer(ClassificationScorer):

    def calculate_similarity(self, actual_class, predicted_class):
        return 1 if any(t in class_predicted for t in class_expected) else 0

    def label(self):
        return "tolerant"
