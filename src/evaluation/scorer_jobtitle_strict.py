from src.evaluation.scorer import Scorer


class StrictJobtitleScorer(Scorer):
    TITLE = "strict evaluation"
    DESCRIPTION = """requires an exact match between the predicted and the actual class (i.e. 1:1). 
    The evaluation result of a single item is 1 if the prediction was correct or 0 if the prediction was false"""

    def calculate_similarity(self, actual_class, predicted_class):
        return int(actual_class == predicted_class)

    def title(self):
        return self.TITLE

    def description(self):
        return self.DESCRIPTION

    def label(self):
        return "strict"
