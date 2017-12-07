from src.evaluation.classification_scorer import ClassificationScorer


class StrictLoeClassificationScorer(ClassificationScorer):
    def calculate_similarity(self, loe_actual, loe_predicted):
        return int(loe_actual == loe_predicted)

    def label(self):
        return "strict"
