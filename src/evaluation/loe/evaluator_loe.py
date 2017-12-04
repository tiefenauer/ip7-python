from src.database.ClassificationResults import LoeClassificationResults
from src.evaluation.evaluator import Evaluator
from src.evaluation.loe.loe_classification_scorer_linear import LinearLoeClassificationScorer
from src.evaluation.loe.loe_classification_scorer_strict import StrictLoeClassificationScorer
from src.evaluation.loe.loe_classification_scorer_tolerant import TolerantLoeClassificationScorer


class LoeEvaluator(Evaluator):

    def __init__(self, args, classifier):
        self.scorer_strict = StrictLoeClassificationScorer(classifier.label())
        self.scorer_tolerant = TolerantLoeClassificationScorer(classifier.label())
        self.scorer_linear = LinearLoeClassificationScorer(classifier.label())
        super(LoeEvaluator, self).__init__(args, classifier, LoeClassificationResults())

    def get_scorers(self):
        return [self.scorer_strict, self.scorer_tolerant, self.scorer_linear]

    def calculate_scores(self, class_expected, class_predicted):
        score_strict = self.scorer_strict.calculate_score(class_expected, class_predicted)
        score_tolerant = self.scorer_tolerant.calculate_score(class_expected, class_predicted)
        score_linear = self.scorer_linear.calculate_score(class_expected, class_predicted)
        return score_strict, score_tolerant, score_linear

    def is_classified(self, predicted_class):
        return predicted_class and len(predicted_class) > 0
