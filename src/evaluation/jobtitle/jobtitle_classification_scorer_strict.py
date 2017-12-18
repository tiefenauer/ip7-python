from src.evaluation.classification_scorer import ClassificationScorer


class StrictJobtitleClassificationScorer(ClassificationScorer):
    def __init__(self):
        super(StrictJobtitleClassificationScorer, self).__init__(label='strict')

    def calculate_similarity(self, actual_class, predicted_class):
        return int(actual_class == predicted_class)
