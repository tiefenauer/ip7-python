from src.classifier.classifier import Classifier


class JobtitleClassifier(Classifier):
    """Uses row.title attribute as the actual class"""

    def get_actual_class(self, row):
        return row.title
