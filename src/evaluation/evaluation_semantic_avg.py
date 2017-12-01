from src.database.ClassificationResults import SemanticAvgClassificationResults
from src.evaluation.evaluation import Evaluation


class SemanticAVGEvaluation(Evaluation):
    def __init__(self, args, data_processor):
        super(SemanticAVGEvaluation, self).__init__(args, data_processor, SemanticAvgClassificationResults())