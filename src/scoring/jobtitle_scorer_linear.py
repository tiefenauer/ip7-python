from src.scoring.scorer_linear import LinearScorer
from src.util import jobtitle_util


class LinearJobtitleScorer(LinearScorer):
    scores = 0

    def _calculate_similarity(self, actual_class, predicted_class):
        """calculates similarity as number of words in predicted class that also appear in actual class"""
        if not predicted_class or len(predicted_class) == 0:
            return 0

        actual_words = list(jobtitle_util.normalize_job_title(actual_class))
        if len(actual_words) == 0:
            return 0
        predicted_words = jobtitle_util.normalize_job_title(predicted_class)
        count = 0

        for word in predicted_words:
            # whole match on word
            if word in actual_words:
                count += 1
            # partial match on word
            elif any(word in actual_word for actual_word in actual_words):
                count += 0.5
        return count / len(actual_words)

    def update_accuracy(self, last_score):
        self.scores += last_score
        if self.total_classified > 0:
            self.accuracy = self.scores / self.total_classified
        self.overall_accuracy = self.scores / (self.total_classified + self.total_unclassified)
        return self.accuracy

    def status(self):
        return 'average accuracy: {}'.format("{:1.4f}".format(self.accuracy))
