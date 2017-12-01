from src.database.ClassificationResults import SemanticRfClassificationResults
from src.evaluation.evaluator import Evaluator


class SemanticRFEvaluation(Evaluator):
    def __init__(self, args, classifier):
        super(SemanticRFEvaluation, self).__init__(args, classifier, SemanticRfClassificationResults())
