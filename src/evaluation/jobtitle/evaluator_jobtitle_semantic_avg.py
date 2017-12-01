from src.database.ClassificationResults import SemanticAvgClassificationResults
from src.evaluation.evaluator import Evaluator


class SemanticAVGEvaluation(Evaluator):
    def __init__(self, args, classifier):
        super(SemanticAVGEvaluation, self).__init__(args, classifier, SemanticAvgClassificationResults())