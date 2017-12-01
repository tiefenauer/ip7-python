from src.database.ClassificationResults import LoeClassificationResults
from src.evaluation.evaluation import Evaluation


class LoeEvaluation(Evaluation):
    def __init__(self, args, data_processor):
        super(LoeEvaluation, self).__init__(args, data_processor, LoeClassificationResults())
