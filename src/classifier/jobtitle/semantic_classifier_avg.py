import logging

import gensim

from src.classifier.jobtitle.semantic_classifier import SemanticClassifier

log = logging.getLogger(__name__)


class SemanticClassifierAvg(SemanticClassifier):
    def classify(self, row):
        feature_vec = self.to_average_vector(row.processed, self.model)
        # query w2v model
        top10 = self.model.similar_by_vector(feature_vec, 1)
        if top10:
            return next(iter(top10))[0]
        return None

    def _train_model(self, sentences, labels, num_rows):
        log.info('Training Word2Vec model')
        model = self.train_w2v_model(sentences)
        model.init_sims()
        return model

    def _save_model(self, model, path):
        model.wv.save_word2vec_format(path, binary=True)
        return path

    def _load_model(self, path):
        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
        model.init_sims(replace=True)
        return model

    def title(self):
        return 'Semantic Classifier (average vector)'

    def description(self):
        return """Classifies some text according to semantic criteria. The class is determined by calculating the
               average vector over all words from the text (only indexed words)."""

    def label(self):
        return 'semantic_avg'
