from src.evaluation.abstract_evaluator import AbstractEvaluator


class LinearJobTitleEvaluator(AbstractEvaluator):
    DESCRIPTION = """the evaluation result is measured as a degree of similarity between predicted and actual
                    class"""

    def prediction_matches(self, actual_class, predicted_class):
        # TODO: implement linear evaluation
        return True

    def title(self):
        """LINEAR EVALUATION"""

    def description(self):
        return self.DESCRIPTION
