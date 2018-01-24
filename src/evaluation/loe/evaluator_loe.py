from src.database.ClassificationResults import LoeClassificationResults
from src.evaluation.evaluator import Evaluator
from src.scoring.los_scorer_linear import LinearLoeScorer
from src.scoring.los_scorer_strict import StrictLoeScorer
from src.scoring.los_scorer_tolerant import TolerantLoeScorer


class LoeEvaluator(Evaluator):

    def __init__(self, args):
        super(LoeEvaluator, self).__init__(args, LoeClassificationResults())
        self.scorer_strict = StrictLoeScorer()
        self.scorer_tolerant = TolerantLoeScorer()
        self.scorer_linear = LinearLoeScorer()

    def get_scorers(self):
        return [self.scorer_strict, self.scorer_tolerant, self.scorer_linear]

    def calculate_scores(self, class_expected, class_predicted):
        score_strict = self.scorer_strict.calculate_score(class_expected, class_predicted)
        score_tolerant = self.scorer_tolerant.calculate_score(class_expected, class_predicted)
        score_linear = self.scorer_linear.calculate_score(class_expected, class_predicted)
        return score_strict, score_tolerant, score_linear

    def is_classified(self, predicted_class):
        return predicted_class and len(predicted_class) > 0
