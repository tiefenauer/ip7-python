from src.database.ClassificationResults import FtsClassificationResults
from src.evaluation.evaluation import Evaluation


class FtsEvaluation(Evaluation):
    def __init__(self, args, data_processor):
        super(FtsEvaluation, self).__init__(args, data_processor, FtsClassificationResults())
