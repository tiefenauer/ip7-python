import gzip
import itertools
import operator
import pickle

import nltk

from src.classifier.classifier import Classifier
from src.importer.known_jobs_tsv_importer import KnownJobsImporter
from src.util import jobtitle_util

known_jobs = KnownJobsImporter()
# number of nouns/verbs to use as features (i.e. the top n nouns and the top n features)
# --> size of the featureset will be 2n
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


def clean_labels(labels_list):
    for label in labels_list:
        # search known job in label
        for job_name_m in (jobtitle_util.to_male_form(job_name) for job_name in known_jobs):
            if job_name_m in label:
                yield job_name_m
        # known job not found ==> return original label
        yield label


class StructuralClassifier(Classifier):
    def __init__(self, args, preprocessor):
        super(StructuralClassifier, self).__init__(args, preprocessor)

    def classify(self, processed_data):
        features = extract_features(processed_data)
        result = self.model.classify(features)
        return result

    def _train_model(self, processed_data, labels, num_rows):
        cleaned_labels = clean_labels(labels)
        labeled_data = zip(processed_data, cleaned_labels)
        train_set = ((extract_features(words), label) for words, label in labeled_data)
        model = nltk.NaiveBayesClassifier.train(train_set)
        return model

    def _get_filename_postfix(self):
        return ''

    def _save_model(self, model, path):
        pickle.dump(model, open(path, 'wb'))
        return path

    def _load_model(self, path):
        model = None
        with gzip.open(path, 'rb') as f:
            model = pickle.load(f)
        return model

    def title(self):
        return 'Structural classifier'

    def description(self):
        return 'Classifies text according to POS tag patterns'

    def label(self):
        return 'structural_nv'
