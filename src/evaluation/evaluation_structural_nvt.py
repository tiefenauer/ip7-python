from src.database.ClassificationResults import StructuralClassificationNVTResults
from src.evaluation.evaluation import Evaluation


class StructuralNVTEvaluation(Evaluation):
    def __init__(self, args, classifier):
        super(StructuralNVTEvaluation, self).__init__(classifier, StructuralClassificationNVTResults(args))
