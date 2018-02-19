import logging

import numpy

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.model_based_classifier import ModelClassifier
from src.util import util

log = logging.getLogger(__name__)


class JobtitleSemanticClassifier(ModelClassifier, JobtitleClassifier):
    """Predicts a job title by exploiting semantic information from the vacancy. A Word2Vec model is trained as an
    internal model."""
    num_features = 300
    index2word_set = set()

    def __init__(self, model):
        super(JobtitleSemanticClassifier, self).__init__(model)
        self.index2word_set = set(model.index2word)

    def predict_class(self, words_lists):
        # calculate average vector
        words_lists = list(util.flatten(words_lists))
        feature_vec = self.to_average_vector(words_lists, self.model)

        # query w2v model
        top10 = self.model.similar_by_vector(feature_vec, 1)
        if top10:
            return next(iter(top10))[0]
        return None

    def to_average_vector(self, word_list, w2v_model):
        """calculates the average vector for a list of words"""

        feature_vec = numpy.zeros(self.num_features, dtype='float32')
        num_words = 0
        for word in word_list:
            if word in self.index2word_set:
                num_words += 1
                feature_vec = numpy.add(feature_vec, w2v_model[word])
        if num_words > 0:
            feature_vec = numpy.divide(feature_vec, num_words)
        return feature_vec

    def title(self):
        return 'Semantic Classifier (average vectors)'

    def label(self):
        return 'semantic'
