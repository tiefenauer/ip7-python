from src.database.classification_results import StructuralClassificationResults
from src.evaluation.evaluator_jobtitle import JobtitleEvaluator


class StructuralEvaluator(JobtitleEvaluator):
    def __init__(self, args):
        super(StructuralEvaluator, self).__init__(args, StructuralClassificationResults())
