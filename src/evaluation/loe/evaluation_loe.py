from src.database.ClassificationResults import LoeClassificationResults
from src.evaluation.evaluator import Evaluator


class LoeEvaluation(Evaluator):
    def __init__(self, args, classifier):
        super(LoeEvaluation, self).__init__(args, classifier, LoeClassificationResults())
