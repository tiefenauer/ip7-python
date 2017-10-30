from abc import ABC, abstractmethod


class AbstractEvaluator(ABC):
    def __init__(self, threshold=0):
        self.threshold = threshold
        self.total_p = 0
        self.total_n = 0
        self.performance = 0
        self.desc_pattern = "positives={}, negatives={}, performance={}"

    def evaluate(self, actual_class, predicted_class):
        if self.calculate_score(actual_class, predicted_class):
            self.total_p += 1
        else:
            self.total_n += 1
        self.performance = self.total_p / (self.total_p + self.total_n)

    def status(self):
        return self.desc_pattern.format(self.total_p, self.total_n, "{:1.4f}".format(self.performance))

    @abstractmethod
    def calculate_score(self, actual_class, predicted_class):
        """check if predicted class matches expected class"""

    @abstractmethod
    def title(self):
        """return a short title of the evaluator"""

    @abstractmethod
    def description(self):
        """describe method of evaluation"""
