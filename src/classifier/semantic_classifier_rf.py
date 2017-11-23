import logging
import pickle

import numpy
from sklearn.ensemble import RandomForestClassifier

from src.classifier.semantic_classifier import SemanticClassifier

log = logging.getLogger(__name__)


class SemanticClassifierRF(SemanticClassifier):
    def classify(self, processed_data):
        # TODO: predict a single item, not the whole matrix!
        pass

    def _train_model(self, sentences, labels, num_rows):
        super(SemanticClassifierRF, self)._train_model(sentences, labels, num_rows)
        # use the trained Word2Vec model to train a RandomForest
        train_data_vecs = self.create_average_vectors(sentences, num_rows)
        forest = RandomForestClassifier(n_estimators=100)
        forest.fit(train_data_vecs, list(labels))
        # Use trained RF as model for this classifier
        self.model = forest
        self.save_model()

    def create_average_vectors(self, sentences, num_rows):
        counter = 0
        avg_feature_vecs = numpy.zeros((num_rows, self.num_features), dtype="float32")
        for row in sentences:
            if counter % 1000 == 0:
                log.info("Vectorized {} of {}".format(counter, num_rows))
            avg_feature_vecs[counter] = self.to_average_vector(row.processed)
            counter += 1
        return avg_feature_vecs

    def _save_model(self, path):
        pickle.dump(path, open(path, 'wb'))
        return path

    def description(self):
        return """Classifies a vacancy by using a RandomForest that has been trained on the average vector of 
        vacancies """

    def title(self):
        return 'Semantic Classifier (Random Forest)'

    def label(self):
        return 'semantic_rf'
