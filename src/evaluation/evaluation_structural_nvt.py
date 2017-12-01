from src.database.ClassificationResults import StructuralClassificationNVTResults
from src.evaluation.evaluation import Evaluation


class StructuralNVTEvaluation(Evaluation):
    def __init__(self, args, data_processor):
        super(StructuralNVTEvaluation, self).__init__(args, data_processor, StructuralClassificationNVTResults())
