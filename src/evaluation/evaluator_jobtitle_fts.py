from src.database.classification_results import FtsClassificationResults
from src.evaluation.evaluator_jobtitle import JobtitleEvaluator


class JobtitleFtsEvaluator(JobtitleEvaluator):
    def __init__(self, args):
        super(JobtitleFtsEvaluator, self).__init__(args, FtsClassificationResults())
