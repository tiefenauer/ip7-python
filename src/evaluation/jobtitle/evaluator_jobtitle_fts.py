from src.database.ClassificationResults import FtsClassificationResults
from src.evaluation.evaluator import Evaluator


class JobtitleFtsEvaluator(Evaluator):
    def __init__(self, args, classifier):
        super(JobtitleFtsEvaluator, self).__init__(args, classifier, FtsClassificationResults())
