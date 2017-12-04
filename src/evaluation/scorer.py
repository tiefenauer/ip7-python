from abc import ABC, abstractmethod


class Scorer(ABC):
    def __init__(self, label='scorer', threshold=0):
        self.lbl = label
        self.threshold = threshold
        self.total_classified = 0
        self.total_unclassified = 0
        self.overall_accuracy = 0
        self.accuracy = 0
        self.desc_pattern = "positives={}, negatives={}, performance={}"

    def update_accuracy(self, last_score):
        self.overall_accuracy = self.total_classified / (self.total_classified + self.total_unclassified)
        self.accuracy = self.overall_accuracy

    def status(self):
        return self.desc_pattern.format(self.total_classified, self.total_unclassified,
                                        "{:1.4f}".format(self.overall_accuracy))

    @abstractmethod
    def calculate_score(self, actual_class, predicted_class):
        """calculate score for a given row"""
        return

    def label(self):
        return self.lbl
