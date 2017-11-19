import nltk

from src.classifier.classifier import Classifier


def extract_features(tagged_words):
    tree = nltk.ne_chunk(tagged_words)
    return tagged_words


class StructuralClassifier(Classifier):
    def classify(self, data):
        pass

    def _load_model(self, filename):
        pass

    def _save_model(self, model, binary, zipped):
        pass

    def _train_model(self, data):
        train_set = [(extract_features(row.processed), row.title) for row in data]
        model = nltk.NaiveBayesClassifier.train(train_set)

    def title(self):
        return 'Structural classifier'

    def description(self):
        return 'Classifies text according to POS tag patterns'

    def label(self):
        'structural (POS)'
