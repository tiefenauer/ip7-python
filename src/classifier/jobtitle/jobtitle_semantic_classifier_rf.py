import logging
import os
import pickle

import numpy
from sklearn.ensemble import RandomForestClassifier

from src.classifier.classifier import data_dir
from src.classifier.jobtitle.jobtitle_semantic_classifier import JobtitleSemanticClassifier
from src.classifier.jobtitle.jobtitle_semantic_classifier_avg import JobtitleSemanticClassifierAvg
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor

log = logging.getLogger(__name__)


class JobtitleSemanticClassifierRF(JobtitleSemanticClassifier):
    """Classifies a vacancy by using the average vectors of vacancies to train a RandomForest. The random forest
    is used as the internal model and overrides the Word2Vec model once the forest has been trained .
    """

    def __init__(self, args, preprocessor=SemanticPreprocessor(remove_stopwords=False)):
        super(JobtitleSemanticClassifierRF, self).__init__(args, preprocessor)
        self.w2v_model = None
        if hasattr(args, 'w2vmodel') and args.w2vmodel:
            self.filename = args.w2vmodel
            self.w2v_model = JobtitleSemanticClassifierAvg(args).load_model()
            log.info('loaded pre-trained Word2Vec-Model')

    def classify(self, word_list):
        # TODO: predict a single item, not the whole matrix!
        pass

    def train_model(self, processed_rows, labels, num_rows):
        # use pre-trained W2V-Model, if available
        if self.w2v_model:
            log.info('using pre-trained W2V-Model')
            w2v_model = self.w2v_model
        else:
            w2v_model = self.train_w2v_model(processed_rows)
        # use the trained Word2Vec model to train a RandomForest
        path = os.path.join(data_dir, 'vecs')
        if os.path.exists(path):
            log.info('loading vectors from file')
            vecs_labels = pickle.load(open(path, 'rb'))
            vecs = [vec for (vec, label) in vecs_labels]
            labels = [label for (vec, label) in vecs_labels]
        else:
            vecs = self.create_average_vectors(w2v_model, processed_rows, num_rows)
            labels = list(labels)
            log.info('Saving vectors for later use')
            pickle.dump(list(zip(vecs, labels)), open(path, 'wb'))

        log.info('loaded {} vecs and {} labels'.format(len(vecs), len(labels)))
        log.info('Training Random Forest...')
        forest = RandomForestClassifier(n_estimators=50, verbose=3)
        forest.fit(vecs, labels)
        log.info('...done!')
        # Use trained RF as model for this classifier
        self.model = forest
        self.save_model()

    def create_average_vectors(self, w2v_model, rows, num_rows):
        counter = 0
        avg_feature_vecs = numpy.zeros((num_rows, self.num_features), dtype="float32")
        for row in rows:
            if counter % 1000 == 0:
                log.info("Vectorized {} of {}".format(counter, num_rows))
            avg_feature_vecs[counter] = self.to_average_vector(row, w2v_model)
            counter += 1
        return avg_feature_vecs

    def serialize_model(self, model, path):
        pickle.dump(model, open(path, 'wb'))
        return path

    def deserialize_model(self, path):
        return pickle.load(open(path, 'rb'))

    def title(self):
        return 'Semantic Classifier (Random Forest)'

    def label(self):
        return 'semantic_rf'
