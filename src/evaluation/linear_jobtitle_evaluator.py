from src import preproc
from src.evaluation.abstract_evaluator import AbstractEvaluator
from src.jobtitle import jobtitle_matcher


class LinearJobTitleEvaluator(AbstractEvaluator):
    TITLE = """linear Evaluation"""
    DESCRIPTION = """the evaluation result is measured as a degree of similarity between predicted and actual
                    class"""
    scores = 0

    def update_accuracy(self, last_score):
        self.scores += last_score
        self.accuracy = self.scores / (self.total_p + self.total_n)
        return self.accuracy

    def status(self):
        return 'average accuracy: {}'.format("{:1.4f}".format(self.accuracy))

    def calculate_score(self, actual_class, predicted_class):
        if not predicted_class or len(predicted_class) == 0:
            return 0

        actual_words = list(self.normalize(actual_class))
        predicted_words = self.normalize(predicted_class)
        count = 0

        for word in predicted_words:
            if word in actual_words:
                count += 1
        return count / len(actual_words)

    def normalize(self, text):
        no_special_chars = preproc.remove_special_chars(text)
        words = preproc.to_words(no_special_chars)
        no_stopwords = (preproc.remove_stop_words(words))
        no_gender = (jobtitle_matcher.to_male_form(word) for word in no_stopwords)
        return (word for word in preproc.stem(no_gender))

    def title(self):
        return self.TITLE

    def description(self):
        return self.DESCRIPTION

    def label(self):
        return "linear"