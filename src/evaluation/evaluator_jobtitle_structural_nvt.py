from src.database.classification_results import StructuralClassificationNVTResults
from src.evaluation.evaluator_jobtitle import JobtitleEvaluator


class StructuralNVTEvaluator(JobtitleEvaluator):
    def __init__(self, args):
        super(StructuralNVTEvaluator, self).__init__(args, StructuralClassificationNVTResults())
