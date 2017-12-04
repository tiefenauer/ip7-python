from src import preproc
from src.evaluation.classification_scorer import ClassificationScorer
from src.util import jobtitle_util


class LinearClassificationScorer(ClassificationScorer):
    scores = 0

    def calculate_similarity(self, actual_class, predicted_class):
        """calculates similarity as number of words in predicted class that also appear in actual class"""
        if not predicted_class or len(predicted_class) == 0:
            return 0

        actual_words = list(self.normalize(actual_class))
        if len(actual_words) == 0:
            return 0
        predicted_words = self.normalize(predicted_class)
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

    def normalize(self, text):
        no_special_chars = preproc.remove_special_chars(text)
        words = preproc.to_words(no_special_chars)
        no_stopwords = (preproc.remove_stop_words(words))
        no_gender = (jobtitle_util.to_male_form(word) for word in no_stopwords)
        return (word for word in preproc.stem(no_gender))

    def label(self):
        return "linear"
