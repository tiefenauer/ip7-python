from src.classifier.classifier import Classifier


class LoeClassifier(Classifier):
    def get_actual_class(self, row):
        return row.workquota_min, row.workquota_max