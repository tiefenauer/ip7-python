from src.database.ClassificationResults import SemanticAvgClassificationResults
from src.evaluation.evaluation import Evaluation


class SemanticAVGEvaluation(Evaluation):
    def __init__(self, args, classifier):
        super(SemanticAVGEvaluation, self).__init__(classifier, SemanticAvgClassificationResults(args))