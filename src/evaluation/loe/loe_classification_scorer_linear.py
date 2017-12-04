from src.evaluation.classification_scorer import ClassificationScorer


class LinearLoeClassificationScorer(ClassificationScorer):
    scores = 0

    def calculate_similarity(self, loe_actual, loe_predicted):
        return 0

    def label(self):
        return "linear"
