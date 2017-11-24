from src.classifier.structural_classifier import StructuralClassifier


class StructuralClassifierNVT(StructuralClassifier):
    def extract_features(self, tagged_words):
        pass

    def title(self):
        return 'Structural Classifier (POS-Tags + HTML Tags)'

    def label(self):
        return 'structural_nvt'

    def description(self):
        return """Classifies text according to POS tag patterns and HTML tags. HTML tags are used as features.
        The n most frequent nouns and verbs are extracted as features. 
        """