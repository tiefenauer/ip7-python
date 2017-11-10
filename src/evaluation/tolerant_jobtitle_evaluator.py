from src.evaluation.abstract_evaluator import AbstractEvaluator


class TolerantJobtitleEvaluator(AbstractEvaluator):
    TITLE = """tolerant evaluation"""
    DESCRIPTION = """allows for some tolerance between predicted and actual class. The evaluation result
                    of a single item is 1 if the prediction is within the tolerance or 0 if not."""

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
