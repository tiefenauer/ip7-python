import logging

import sys

from gensim.models import word2vec

from src.classifier.classification_strategy import ClassificationStrategy

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class SemanticClassifier(ClassificationStrategy):
    def train(self, sentences):
        logging.info('Training Word2Vec model')
        num_features = 300
        min_word_count = 40
        num_workers = 6
        context = 10
        downsampling = 1e-3
        model = word2vec.Word2Vec(sentences,
                                  workers=num_workers,
                                  size=num_features,
                                  min_count=min_word_count,
                                  window=context,
                                  sample=downsampling
                                  )
        model.init_sims()
        model_name = '300features_40minwords_10context'
        model.save(model_name)

    def title(self):
        return 'Semantic Classifier'

    def classify(self, data):
        pass

    def description(self):
        return 'classifies some text according to semantic criteria'

    def label(self):
        return 'semantic'
