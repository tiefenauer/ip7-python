from src.classifier.classifier import Classifier


class JobtitleClassifier(Classifier):
    def get_actual_class(self, row):
        return row.title
