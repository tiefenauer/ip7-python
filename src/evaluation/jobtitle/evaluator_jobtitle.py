from src.evaluation.evaluator import Evaluator
from src.evaluation.scorer_jobtitle_linear import LinearJobTitleScorer
from src.evaluation.scorer_jobtitle_strict import StrictJobtitleScorer
from src.evaluation.scorer_jobtitle_tolerant import TolerantJobtitleScorer


class JobtitleEvaluator(Evaluator):

    def __init__(self, args, classifier, results):
        self.scorer_strict = StrictJobtitleScorer(classifier)
        self.scorer_tolerant = TolerantJobtitleScorer(classifier)
        self.scorer_linear = LinearJobTitleScorer(classifier)
        super(JobtitleEvaluator, self).__init__(args, classifier, results)

    def get_scorers(self):
        return [self.scorer_strict, self.scorer_tolerant, self.scorer_linear]

    def calculate_scores(self, row):
        class_expected = row.title
        class_predicted = row.predicted_class
        score_strict = self.scorer_strict.score(class_expected, class_predicted)
        score_tolerant = self.scorer_tolerant.score(class_expected, class_predicted)
        score_linear = self.scorer_linear.score(class_expected, class_predicted)
        return score_strict, score_tolerant, score_linear

    def is_classified(self, row):
        return row.predicted_class and len(row.predicted_class) > 0
