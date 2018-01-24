from abc import ABC, abstractmethod

desc_pattern = "positives={}, negatives={}, performance={}"


class Scorer(ABC):
    def __init__(self, label, threshold=0):
        self.label = label
        self.threshold = threshold
        self.total_classified = 0
        self.total_unclassified = 0
        self.overall_accuracy = 0
        self.accuracy = 0

    def calculate_score(self, actual_class, predicted_class):
        score = self.calculate_similarity(actual_class, predicted_class)
        if score > self.threshold:
            self.total_classified += 1
        else:
            self.total_unclassified += 1
        self.update_accuracy(score)
        # score might be > 1 if prediction contains the actual class multiple times
        return min(score, 1)

    def update_accuracy(self, last_score):
        self.overall_accuracy = self.total_classified / (self.total_classified + self.total_unclassified)
        self.accuracy = self.overall_accuracy

    def status(self):
        return desc_pattern.format(self.total_classified, self.total_unclassified,
                                   "{:1.4f}".format(self.overall_accuracy))

    def calculate_similarity(self, actual_class, predicted_class):
        # score might be > 1 if prediction contains the actual class multiple times
        score = self._calculate_similarity(actual_class, predicted_class)
        return min(score, 1)

    @abstractmethod
    def _calculate_similarity(self, actual_class, predicted_class):
        """calculate how closely the predicted class matches the expected class"""
        return 0

    def label(self):
        return self.label
