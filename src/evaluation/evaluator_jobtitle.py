from src.evaluation.evaluator import Evaluator
from src.scoring.jobtitle_scorer_linear import LinearJobtitleScorer
from src.scoring.jobtitle_scorer_strict import StrictJobtitleScorer
from src.scoring.jobtitle_scorer_tolerant import TolerantJobtitleScorer


class JobtitleEvaluator(Evaluator):

    def __init__(self, args, ResultEntity):
        super(JobtitleEvaluator, self).__init__(args, ResultEntity)
        self.scorer_strict = StrictJobtitleScorer()
        self.scorer_tolerant = TolerantJobtitleScorer()
        self.scorer_linear = LinearJobtitleScorer()

    def get_scorers(self):
        return [self.scorer_strict, self.scorer_tolerant, self.scorer_linear]

    def calculate_scores(self, class_expected, class_predicted):
        score_strict = self.scorer_strict.calculate_score(class_expected, class_predicted)
        score_tolerant = self.scorer_tolerant.calculate_score(class_expected, class_predicted)
        score_linear = self.scorer_linear.calculate_score(class_expected, class_predicted)
        return score_strict, score_tolerant, score_linear

    def is_classified(self, predicted_class):
        return predicted_class and len(predicted_class) > 0
