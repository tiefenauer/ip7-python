import logging

import gensim

from src.classifier.jobtitle.jobtitle_semantic_classifier import JobtitleSemanticClassifier
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor

log = logging.getLogger(__name__)


class JobtitleSemanticClassifierAvg(JobtitleSemanticClassifier):
    """Predicts a jobtitle using a pre-trained Word2Vec model. The classification is made by calculating the average
    of all word vectors from the vacancy that are indexed in the model."""

    def classify(self, word_list):
        feature_vec = self.to_average_vector(word_list, self.model)
        # query w2v model
        top10 = self.model.similar_by_vector(feature_vec, 1)
        if top10:
            return next(iter(top10))[0]
        return None

    def train_model(self, train_data):
        sentences = TrainingSentences(self.preprocessor(train_data))
        model = self.train_w2v_model(sentences)
        return model

    def serialize_model(self, model, path):
        """serialize model using built-in save functionality from gensim"""
        model.wv.save_word2vec_format(path, binary=True)
        return path

    def deserialize_model(self, path):
        """de serialize model using built-in load functionality from gensim"""
        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
        model.init_sims(replace=True)
        return model

    def title(self):
        return 'Semantic Classifier (average vectors)'

    def label(self):
        return 'semantic_avg'


class TrainingSentences(object):
    """helper class to train Word2Vec model using pre-processed data
    This class is needed because Word2Vec expects an iterator returning a sentence as a list of words in each iteration
    The default SemenaticProcessor information however is implemented as a generator returning the whole row and the
    tokenized words as a generator in each iteration. This behavior is needed in evaluating because there the expected
    target label is needed.
    To train the Word2Vec we expects an iterator (not a generator) returning a list of tokenized words (not a generator)
    for training!
    """

    def __init__(self, processed_rows):
        self.processed_rows = processed_rows

    def __iter__(self):
        for row in self.processed_rows:
            # evaluate generator
            yield list(row.processed)
