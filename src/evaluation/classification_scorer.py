from abc import abstractmethod

from src.evaluation.scorer import Scorer


class ClassificationScorer(Scorer):

    def calculate_score(self, actual_class, predicted_class):
        score = self.calculate_similarity(actual_class, predicted_class)
        if score > self.threshold:
            self.total_classified += 1
        else:
            self.total_unclassified += 1
        self.update_accuracy(score)
        return score

    @abstractmethod
    def calculate_similarity(self, actual_class, predicted_class):
        """calculate how closely the predicted class matches the expected class"""
