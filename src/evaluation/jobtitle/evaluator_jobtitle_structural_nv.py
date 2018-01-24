from src.database.ClassificationResults import StructuralClassificationNVResults
from src.evaluation.jobtitle.evaluator_jobtitle import JobtitleEvaluator


class StructuralNVEvaluator(JobtitleEvaluator):
    def __init__(self, args):
        super(StructuralNVEvaluator, self).__init__(args, StructuralClassificationNVResults())
