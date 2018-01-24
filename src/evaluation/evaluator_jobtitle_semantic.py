from src.database.classification_results import SemanticClassificationResults
from src.evaluation.evaluator_jobtitle import JobtitleEvaluator


class SemanticEvaluation(JobtitleEvaluator):
    def __init__(self, args):
        super(SemanticEvaluation, self).__init__(args, SemanticClassificationResults())
