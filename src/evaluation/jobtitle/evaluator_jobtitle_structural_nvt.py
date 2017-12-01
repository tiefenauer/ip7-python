from src.database.ClassificationResults import StructuralClassificationNVTResults
from src.evaluation.evaluator import Evaluator


class StructuralNVTEvaluation(Evaluator):
    def __init__(self, args, classifier):
        super(StructuralNVTEvaluation, self).__init__(args, classifier, StructuralClassificationNVTResults())
