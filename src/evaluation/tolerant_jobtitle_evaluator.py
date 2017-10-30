from src.evaluation.abstract_evaluator import AbstractEvaluator


class TolerantJobtitleEvaluator(AbstractEvaluator):
    TITLE = """tolerant evaluation"""
    DESCRIPTION = """allows for some tolerance between predicted and actual class. The evaluation result
                    of a single item is 1 if the prediction is within the tolerance or 0 if not."""

    def calculate_score(self, actual_class, predicted_class):
        if not predicted_class:
            return False
        return predicted_class in actual_class

    def title(self):
        return self.TITLE

    def description(self):
        return self.DESCRIPTION

    def label(self):
        return "tolerant"
