from src.evaluation.scorer import Scorer


class TolerantJobtitleScorer(Scorer):

    def calculate_similarity(self, actual_class, predicted_class):
        similarity = 0
        if predicted_class and predicted_class in actual_class:
            similarity = 1
        return similarity

    def title(self):
        return self.TITLE

    def description(self):
        return self.DESCRIPTION

    def label(self):
        return "tolerant"
