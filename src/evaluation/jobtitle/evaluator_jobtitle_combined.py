from src.database.ClassificationResults import CombinedClassificatoinResults
from src.evaluation.jobtitle.evaluator_jobtitle import JobtitleEvaluator


class JobtitleCombinedEvaluator(JobtitleEvaluator):
    def __init__(self, args, classifier):
        super(JobtitleCombinedEvaluator, self).__init__(args, classifier, CombinedClassificatoinResults())
