import logging
from abc import abstractmethod

import numpy
from gensim.models import word2vec

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.model_classifier import ModelClassifier

log = logging.getLogger(__name__)


class JobtitleSemanticClassifier(ModelClassifier, JobtitleClassifier):
    """Predicts a job title by exploiting semantic information from the vacancy. A Word2Vec model is trained as an
    internal model."""

    def __init__(self, args):
        super(JobtitleSemanticClassifier, self).__init__(args)
        self.num_features = 300
        self.min_word_count = 40
        self.context = 10
        self.num_workers = 6
        self.downsampling = 1e-3

    def train_w2v_model(self, sentences):
        """trains a new Word2Vec model"""
        log.info('Training new Word2Vec model...')

        model = word2vec.Word2Vec(sentences,
                                  workers=self.num_workers,
                                  size=self.num_features,
                                  min_count=self.min_word_count,
                                  window=self.context,
                                  sample=self.downsampling
                                  )
        model.init_sims()

        log.info('...done!')
        return model

    def to_average_vector(self, word_list, w2v_model):
        """calculates the average vector for a list of words"""

        feature_vec = numpy.zeros(self.num_features, dtype='float32')
        num_words = 0
        index2word_set = set(w2v_model.index2word)
        for word in word_list:
            if word in index2word_set:
                num_words += 1
                feature_vec = numpy.add(feature_vec, w2v_model[word])
        if num_words > 0:
            feature_vec = numpy.divide(feature_vec, num_words)
        return feature_vec

    def get_filename_postfix(self):
        return '{features}features_{minwords}minwords_{context}context'.format(features=self.num_features,
                                                                               minwords=self.min_word_count,
                                                                               context=self.context)

    @abstractmethod
    def predict_class(self, word_list):
        """to be implemented in subclass"""
        return
