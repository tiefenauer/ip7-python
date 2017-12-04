from src.database.ClassificationResults import FtsClassificationResults
from src.evaluation.jobtitle.evaluator_jobtitle import JobtitleEvaluator


class JobtitleFtsEvaluator(JobtitleEvaluator):
    def __init__(self, args, classifier):
        super(JobtitleFtsEvaluator, self).__init__(args, classifier, FtsClassificationResults())
