from src.database.ClassificationResults import SemanticAvgClassificationResults
from src.evaluation.jobtitle.evaluator_jobtitle import JobtitleEvaluator


class SemanticAVGEvaluation(JobtitleEvaluator):
    def __init__(self, args, classifier):
        super(SemanticAVGEvaluation, self).__init__(args, classifier, SemanticAvgClassificationResults())