from src.database.ClassificationResults import StructuralClassificationNVResults
from src.evaluation.evaluation import Evaluation


class StructuralNVEvaluation(Evaluation):
    def __init__(self, args, classifier):
        super(StructuralNVEvaluation, self).__init__(args, classifier, StructuralClassificationNVResults())
