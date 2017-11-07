from abc import ABC, abstractmethod


class AbstractEvaluator(ABC):
    def __init__(self, threshold=0):
        self.threshold = threshold
        self.total_classified = 0
        self.total_unclassified = 0
        self.overall_accuracy = 0
        self.accuracy = 0
        self.desc_pattern = "positives={}, negatives={}, performance={}"

    def evaluate(self, actual_class, predicted_class):
        score = self.calculate_similarity(actual_class, predicted_class)
        if score > self.threshold:
            self.total_classified += 1
        else:
            self.total_unclassified += 1
        self.update_accuracy(score)
        return score

    def update_accuracy(self, last_score):
        self.overall_accuracy = self.total_classified / (self.total_classified + self.total_unclassified)
        self.accuracy = self.overall_accuracy

    def status(self):
        return self.desc_pattern.format(self.total_classified, self.total_unclassified, "{:1.4f}".format(self.overall_accuracy))

    @abstractmethod
    def calculate_similarity(self, actual_class, predicted_class):
        """calculate how closely the predicted class matches the expected class"""

    @abstractmethod
    def title(self):
        """return a short title of the evaluator"""

    @abstractmethod
    def description(self):
        """describe method of evaluation"""

    @abstractmethod
    def label(self):
        """label for visualisaiton"""