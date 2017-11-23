import logging

import gensim
import numpy
from gensim.models import word2vec

from src.classifier.classifier import Classifier
from src.preprocessing.preprocessor_semantic import SemanticX28Preprocessor

log = logging.getLogger(__name__)


class SemanticClassifier(Classifier):
    def __init__(self, args, preprocessor=SemanticX28Preprocessor(remove_stopwords=False)):
        super(SemanticClassifier, self).__init__(args, preprocessor)
        self.num_features = 300
        self.min_word_count = 40
        self.num_workers = 6
        self.context = 10
        self.downsampling = 1e-3

    def _train_model(self, sentences, labels, num_rows):
        log.info('Training Word2Vec model')
        model = word2vec.Word2Vec(sentences,
                                  workers=self.num_workers,
                                  size=self.num_features,
                                  min_count=self.min_word_count,
                                  window=self.context,
                                  sample=self.downsampling
                                  )
        model.init_sims()
        return model

    def _save_model(self, path):
        self.model.wv.save_word2vec_format(path, binary=True)
        self.index2word_set = set(model.index2word)
        return path

    def _load_model(self, path):
        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
        model.init_sims(replace=True)
        self.index2word_set = set(model.index2word)
        return model

    def _get_filename_postfix(self):
        return '{features}features_{minwords}minwords_{context}context'.format(features=self.num_features,
                                                                               minwords=self.min_word_count,
                                                                               context=self.context)

    def to_average_vector(self, processed_row):
        feature_vec = numpy.zeros(self.num_features, dtype='float32')
        num_words = 0
        for word in processed_row:
            if word in self.index2word_set:
                num_words += 1
                feature_vec = numpy.add(feature_vec, self.model[word])
        if num_words > 0:
            feature_vec = numpy.divide(feature_vec, num_words)
        return feature_vec
