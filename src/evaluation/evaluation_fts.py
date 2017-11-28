from src.database.ClassificationResults import FtsClassificationResults
from src.evaluation.evaluation import Evaluation


class FtsEvaluation(Evaluation):
    def __init__(self, args, classifier):
        super(FtsEvaluation, self).__init__(classifier, FtsClassificationResults(args))
