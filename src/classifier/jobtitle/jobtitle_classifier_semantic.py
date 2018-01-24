import logging

import numpy
from gensim.models import word2vec

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.model_classifier import ModelClassifier

log = logging.getLogger(__name__)


class JobtitleSemanticClassifier(ModelClassifier, JobtitleClassifier):
    """Predicts a job title by exploiting semantic information from the vacancy. A Word2Vec model is trained as an
    internal model."""
    num_features = 300
    min_word_count = 20
    context = 10
    num_workers = 6
    downsampling = 1e-3
    index2word_set = set()

    def predict_class(self, words_lists):
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

    def get_filename_postfix(self):
        return '{features}features_{minwords}minwords_{context}context'.format(features=self.num_features,
                                                                               minwords=self.min_word_count,
                                                                               context=self.context)

    def train_model(self, sentences):
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

    def load_model(self):
        model = super(JobtitleSemanticClassifier, self).load_model()
        self.index2word_set = set(model.index2word)
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
