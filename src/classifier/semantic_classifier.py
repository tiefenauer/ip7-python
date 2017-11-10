import gzip
import logging
import os
import shutil
import sys
import time

import gensim
from gensim.models import word2vec

from src.classifier.classification_strategy import ClassificationStrategy, data_dir

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def create_filename(num_features, min_word_count, context):
    fn_ts = time.strftime('%Y-%m-%d-%H-%M-%S')
    fn_parms = '{features}features_{minwords}minwords_{context}context'.format(features=num_features,
                                                                               minwords=min_word_count,
                                                                               context=context)
    filename = fn_ts + '_' + fn_parms
    return os.path.join(data_dir, filename)


class SemanticClassifier(ClassificationStrategy):
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
        return model

    def _save_model(self, model, binary, zipped):
        filename = create_filename(self.num_features, self.min_word_count, self.context)
        model.wv.save_word2vec_format(filename, binary=binary)
        if zipped:
            filename_gz = filename + '.gz'
            with open(filename, 'rb') as f_in, gzip.open(filename_gz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            os.remove(filename)
        return filename_gz

    def _load_model(self, filename):
        model = gensim.models.KeyedVectors.load_word2vec_format(filename, binary=True)
        return model

    def title(self):
        return 'Semantic Classifier'

    def classify(self, data):
        pass

    def description(self):
        return 'classifies some text according to semantic criteria'

    def label(self):
        return 'semantic'
