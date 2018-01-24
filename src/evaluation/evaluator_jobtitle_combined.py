from src.database.classification_results import CombinedClassificationResults
from src.evaluation.evaluator_jobtitle import JobtitleEvaluator


class JobtitleCombinedEvaluator(JobtitleEvaluator):
    def __init__(self, args):
        super(JobtitleCombinedEvaluator, self).__init__(args, CombinedClassificationResults())
