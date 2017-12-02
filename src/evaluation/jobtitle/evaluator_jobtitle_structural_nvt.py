from src.database.ClassificationResults import StructuralClassificationNVTResults
from src.evaluation.jobtitle.evaluator_jobtitle import JobtitleEvaluator


class StructuralNVTEvaluator(JobtitleEvaluator):
    def __init__(self, args, classifier):
        super(StructuralNVTEvaluator, self).__init__(args, classifier, StructuralClassificationNVTResults())