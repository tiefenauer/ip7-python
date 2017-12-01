import logging
from abc import abstractmethod

import numpy
from gensim.models import word2vec

from src.classifier.core.model_classifier import ModelClassifier
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor

log = logging.getLogger(__name__)


class SemanticClassifier(ModelClassifier):
    def __init__(self, args, preprocessor=SemanticPreprocessor(remove_stopwords=False)):
        self.num_features = 300
        self.min_word_count = 40
        self.context = 10
        super(SemanticClassifier, self).__init__(args, preprocessor)
        self.num_workers = 6
        self.downsampling = 1e-3

    def train_w2v_model(self, processed_data):
        sentences = [list(words) for words in processed_data]
        model = word2vec.Word2Vec(sentences,
                                  workers=self.num_workers,
                                  size=self.num_features,
                                  min_count=self.min_word_count,
                                  window=self.context,
                                  sample=self.downsampling
                                  )
        model.init_sims()
        return model

    def to_average_vector(self, processed_row, w2v_model):
        feature_vec = numpy.zeros(self.num_features, dtype='float32')
        num_words = 0
        index2word_set = set(w2v_model.index2word)
        for word in processed_row:
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
    def description(self):
        """to be implemented in subclass"""

    @abstractmethod
    def classify(self, processed_row):
        """to be implemented in subclass"""

    @abstractmethod
    def _load_model(self, path):
        """to be implemented in subclass"""

    @abstractmethod
    def _save_model(self, model, path):
        """to be implemented in subclass"""

    @abstractmethod
    def _train_model(self, processed_data, labels, num_rows):
        """to be implemented in subclass"""

    @abstractmethod
    def title(self):
        pass

    @abstractmethod
    def label(self):
        pass
