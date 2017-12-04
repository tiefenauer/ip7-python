from src.evaluation.classification_scorer_linear import LinearClassificationScorer
from src.evaluation.classification_scorer_strict import StrictClassificationScorer
from src.evaluation.classification_scorer_tolerant import TolerantClassificationScorer
from src.evaluation.evaluator import Evaluator


class JobtitleEvaluator(Evaluator):

    def __init__(self, args, classifier, results):
        self.scorer_strict = StrictClassificationScorer(classifier.label())
        self.scorer_tolerant = TolerantClassificationScorer(classifier.label())
        self.scorer_linear = LinearClassificationScorer(classifier.label())
        super(JobtitleEvaluator, self).__init__(args, classifier, results)

    def get_scorers(self):
        return [self.scorer_strict, self.scorer_tolerant, self.scorer_linear]

    def calculate_scores(self, class_expected, class_predicted):
        score_strict = self.scorer_strict.calculate_score(class_expected, class_predicted)
        score_tolerant = self.scorer_tolerant.calculate_score(class_expected, class_predicted)
        score_linear = self.scorer_linear.calculate_score(class_expected, class_predicted)
        return score_strict, score_tolerant, score_linear

    def is_classified(self, predicted_class):
        return predicted_class and len(predicted_class) > 0
