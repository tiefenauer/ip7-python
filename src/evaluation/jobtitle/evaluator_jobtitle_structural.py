from src.database.ClassificationResults import StructuralClassificationResults
from src.evaluation.jobtitle.evaluator_jobtitle import JobtitleEvaluator


class StructuralNVTEvaluator(JobtitleEvaluator):
    def __init__(self, args):
        super(StructuralNVTEvaluator, self).__init__(args, StructuralClassificationResults())
