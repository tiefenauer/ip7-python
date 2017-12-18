from src.evaluation.evaluator import Evaluator
from src.evaluation.jobtitle.jobtitle_classification_scorer_linear import LinearJobtitleClassificationScorer
from src.evaluation.jobtitle.jobtitle_classification_scorer_strict import StrictJobtitleClassificationScorer
from src.evaluation.jobtitle.jobtitle_classification_scorer_tolerant import TolerantJobtitleClassificationScorer


class JobtitleEvaluator(Evaluator):

    def __init__(self, args, ResultEntity):
        super(JobtitleEvaluator, self).__init__(args, ResultEntity)
        self.scorer_strict = StrictJobtitleClassificationScorer()
        self.scorer_tolerant = TolerantJobtitleClassificationScorer()
        self.scorer_linear = LinearJobtitleClassificationScorer()

    def get_scorers(self):
        return [self.scorer_strict, self.scorer_tolerant, self.scorer_linear]

    def calculate_scores(self, class_expected, class_predicted):
        score_strict = self.scorer_strict.calculate_score(class_expected, class_predicted)
        score_tolerant = self.scorer_tolerant.calculate_score(class_expected, class_predicted)
        score_linear = self.scorer_linear.calculate_score(class_expected, class_predicted)
        return score_strict, score_tolerant, score_linear

    def is_classified(self, predicted_class):
        return predicted_class and len(predicted_class) > 0
