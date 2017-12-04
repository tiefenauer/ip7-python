from src.evaluation.classification_scorer import ClassificationScorer


class TolerantClassificationScorer(ClassificationScorer):

    def calculate_similarity(self, actual_class, predicted_class):
        similarity = 0
        if predicted_class and predicted_class in actual_class:
            similarity = 1
        return similarity

    def label(self):
        return "tolerant"
