from src.database.ClassificationResults import SemanticRfClassificationResults
from src.evaluation.evaluation import Evaluation


class SemanticRFEvaluation(Evaluation):
    def __init__(self, args, data_processor):
        super(SemanticRFEvaluation, self).__init__(args, data_processor, SemanticRfClassificationResults())
