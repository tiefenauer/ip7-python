from src.evaluation.classification_scorer import ClassificationScorer


class StrictJobtitleClassificationScorer(ClassificationScorer):
    def calculate_similarity(self, actual_class, predicted_class):
        return int(actual_class == predicted_class)

    def label(self):
        return "strict"
