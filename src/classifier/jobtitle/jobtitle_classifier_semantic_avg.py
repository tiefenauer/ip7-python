import logging

import gensim

from src.classifier.jobtitle.jobtitle_classifier_semantic import JobtitleSemanticClassifier
from src.util import util

log = logging.getLogger(__name__)


class JobtitleSemanticClassifierAvg(JobtitleSemanticClassifier):
    """Predicts a jobtitle using a pre-trained Word2Vec model. The classification is made by calculating the average
    of all word vectors from the vacancy that are indexed in the model."""

    def predict_class(self, words_lists):
        words_lists = list(util.flatten(words_lists))
        feature_vec = self.to_average_vector(words_lists, self.model)
        # query w2v model
        top10 = self.model.similar_by_vector(feature_vec, 1)
        if top10:
            return next(iter(top10))[0]
        return None

    def train_model(self, sentences):
        """Trains a Word2Vec model using the given pre-processed sentences (list of list of words)"""
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
