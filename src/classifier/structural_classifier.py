import nltk

from src.classifier.classifier import Classifier


def extract_features(tagged_words):
    tree = nltk.ne_chunk(tagged_words)
    return tagged_words


class StructuralClassifier(Classifier):
    def __init__(self, args, preprocessor):
        super(StructuralClassifier, self).__init__(args, preprocessor)

    def classify(self, processed_data):
        pass

    def _load_model(self, path):
        pass

    def _save_model(self, path, binary, zipped):
        pass

    def _train_model(self, processed_data, labels, num_rows):
        train_set = [(extract_features(row.processed), row.title) for row in processed_data]
        model = nltk.NaiveBayesClassifier.train(train_set)

    def title(self):
        return 'Structural classifier'

    def description(self):
        return 'Classifies text according to POS tag patterns'

    def label(self):
        'structural (POS)'
