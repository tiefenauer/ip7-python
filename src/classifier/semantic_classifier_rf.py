import logging
import pickle

import numpy
from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm

from src.classifier.semantic_classifier import SemanticClassifier

log = logging.getLogger(__name__)


class SemanticClassifierRF(SemanticClassifier):
    def classify(self, processed_data):
        # TODO: predict a single item, not the whole matrix!
        pass

    def _train_model(self, sentences, labels, num_rows):
        w2v_model = self.train_w2v_model(sentences)
        # use the trained Word2Vec model to train a RandomForest
        train_data_vecs = self.create_average_vectors(w2v_model, sentences, num_rows)
        log.info('Training Random Forest...')
        forest = RandomForestClassifier(n_estimators=100)
        forest.fit(list(train_data_vecs), list(labels))
        log.info('...done!')
        # Use trained RF as model for this classifier
        self.model = forest
        self.save_model()

    def create_average_vectors(self, w2v_model, sentences, num_rows):
        counter = 0
        avg_feature_vecs = numpy.zeros((num_rows, self.num_features), dtype="float32")
        for row in sentences:
            if counter % 1000 == 0:
                log.info("Vectorized {} of {}".format(counter, num_rows))
            avg_feature_vecs[counter] = self.to_average_vector(row.processed, w2v_model)
            counter += 1
        return avg_feature_vecs

    def _save_model(self, path):
        pickle.dump(path, open(path, 'wb'))
        return path

    def _load_model(self, path):
        return pickle.load(open(path, 'rb'))

    def description(self):
        return """Classifies a vacancy by using a RandomForest that has been trained on the average vector of 
        vacancies """

    def title(self):
        return 'Semantic Classifier (Random Forest)'

    def label(self):
        return 'semantic_rf'
