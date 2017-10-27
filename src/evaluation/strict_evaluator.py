from src.evaluation.abstract_evaluator import AbstractEvaluator


class StrictEvaluator(AbstractEvaluator):
    DESCRIPTION = """requires an exact match between the predicted and the actual class (i.e. 1:1). 
    The evaluation result of a single item is 1 if the prediction was correct or 0 if the prediction was false"""

    def features_match(self, actual_class, predicted_class):
        return actual_class == predicted_class

    def describe_evaluation(self):
        return self.DESCRIPTION
