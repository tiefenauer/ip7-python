import gzip
import logging
import os
import shutil
import sys

import gensim
import numpy as np
from gensim.models import word2vec

from src.classifier.classifier import Classifier
from src.util import semantic_util
from src.util.semantic_util import create_filename

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class SemanticClassifier(Classifier):
    def __init__(self, model_file=None):
        super(SemanticClassifier, self).__init__(model_file)
        self.num_features = 300
        self.min_word_count = 40
        self.num_workers = 6
        self.context = 10
        self.downsampling = 1e-3

    def _train_model(self, sentences):
        logging.info('Training Word2Vec model')
        model = word2vec.Word2Vec(sentences,
                                  workers=self.num_workers,
                                  size=self.num_features,
                                  min_count=self.min_word_count,
                                  window=self.context,
                                  sample=self.downsampling
                                  )
        model.init_sims()
        self.model = model
        return model

    def _save_model(self, model, binary, zipped):
        filename = semantic_util.create_filename(self.num_features, self.min_word_count, self.context)
        model.wv.save_word2vec_format(filename, binary=binary)
        if zipped:
            filename_gz = filename + '.gz'
            with open(filename, 'rb') as f_in, gzip.open(filename_gz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            os.remove(filename)
            return filename_gz
        return filename

    def _load_model(self, path):
        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
        model.init_sims(replace=True)
        self.index2word_set = set(model.index2word)
        return model

    def classify(self, words):
        featureVec = self.makeFeatureVec(words)
        top10 = self.model.similar_by_vector(featureVec,1)
        if top10:
            return next(iter(top10))[0]
        return None

    def makeFeatureVec(self, words):
        featureVec = np.zeros((self.num_features), dtype='float32')
        nwords = 0
        for word in words:
            if word in self.index2word_set:
                nwords += 1
                featureVec = np.add(featureVec, self.model[word])
        featureVec = np.divide(featureVec, nwords)
        return featureVec

    def title(self):
        return 'Semantic Classifier'

    def description(self):
        return 'classifies some text according to semantic criteria'

    def label(self):
        return 'semantic'
