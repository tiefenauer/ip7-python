from src.evaluation.classification_scorer import ClassificationScorer
from src.util import jobtitle_util


class LinearJobtitleClassificationScorer(ClassificationScorer):
    scores = 0

    def __init__(self):
        super(LinearJobtitleClassificationScorer, self).__init__(label='linear')

    def calculate_similarity(self, actual_class, predicted_class):
        """calculates similarity as number of words in predicted class that also appear in actual class"""
        if not predicted_class or len(predicted_class) == 0:
            return 0

        actual_words = list(jobtitle_util.normalize_text(actual_class))
        if len(actual_words) == 0:
            return 0
        predicted_words = jobtitle_util.normalize_text(predicted_class)
        count = 0

        for word in predicted_words:
            if word in actual_words:
                count += 1
        return count / len(actual_words)

    def update_accuracy(self, last_score):
        self.scores += last_score
        if self.total_classified > 0:
            self.accuracy = self.scores / self.total_classified
        self.overall_accuracy = self.scores / (self.total_classified + self.total_unclassified)
        return self.accuracy

    def status(self):
        return 'average accuracy: {}'.format("{:1.4f}".format(self.accuracy))

    def label(self):
        return "linear"
