import itertools
import operator

import nltk

from src.classifier.classifier import Classifier

n = 5


def top_n(tagged_words, tag, n):
    tagged_words_with_tag = (w for (w, t) in tagged_words if t.startswith(tag))
    dct = {k: sum(1 for _ in g) for k, g in itertools.groupby(tagged_words_with_tag)}
    top = sorted(dct.items(), key=operator.itemgetter(1), reverse=True)
    return top[:n]


def extract_features(tagged_words):
    # convert to list because of two passes!
    tagged_words = list(tagged_words)
    top_n_nouns = top_n(tagged_words, 'N', n)
    top_n_verbs = top_n(tagged_words, 'V', n)
    #
    features = {}
    for i, (noun, count) in enumerate(top_n_nouns, 1):
        features['noun-{}'.format(i)] = noun
    for i, (verb, count) in enumerate(top_n_verbs, 1):
        features['verb-{}'.format(i)] = verb
    return features


class StructuralClassifier(Classifier):
    def __init__(self, args, preprocessor):
        super(StructuralClassifier, self).__init__(args, preprocessor)

    def classify(self, processed_data):
        pass

    def _get_filename_postfix(self):
        pass

    def _save_model(self, path):
        pass

    def _load_model(self, path):
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
