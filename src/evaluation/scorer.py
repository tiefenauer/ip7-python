from abc import ABC, abstractmethod


class Scorer(ABC):
    def __init__(self, classifier, threshold=0):
        self.classifier = classifier
        self.threshold = threshold
        self.total_classified = 0
        self.total_unclassified = 0
        self.overall_accuracy = 0
        self.accuracy = 0
        self.desc_pattern = "positives={}, negatives={}, performance={}"

    def evaluate_all(self, ground_truth, predictions):
        for expected_class, predicted_class in zip(ground_truth, predictions):
            self.score(expected_class, predicted_class)
        return self.accuracy

    def score(self, actual_class, predicted_class):
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
        return self.desc_pattern.format(self.total_classified, self.total_unclassified,
                                        "{:1.4f}".format(self.overall_accuracy))

    @abstractmethod
    def calculate_similarity(self, actual_class, predicted_class):
        """calculate how closely the predicted class matches the expected class"""

    def label(self):
        return self.classifier.label()
