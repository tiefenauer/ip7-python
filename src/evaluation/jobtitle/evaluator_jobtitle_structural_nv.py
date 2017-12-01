from src.database.ClassificationResults import StructuralClassificationNVResults
from src.evaluation.evaluator import Evaluator


class StructuralNVEvaluation(Evaluator):
    def __init__(self, args, classifier):
        super(StructuralNVEvaluation, self).__init__(args, classifier, StructuralClassificationNVResults())
