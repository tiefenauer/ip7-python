import argparse
import logging
import sys

from src.classifier.semantic_classifier import SemanticClassifier
from src.database.FetchflowData import FetchflowData
from src.preprocessing.preprocessor_semantic import SemanticX28Preprocessor

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
parser = argparse.ArgumentParser(description="""Train Semantic Classifier (Word2Vec)""")
parser.add_argument('-s', '--split', nargs='?', type=float, default=1.0,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
args = parser.parse_args()


class MySentences(object):
    def __init__(self, rows):
        self.rows = rows

    def __iter__(self):
        for sentences in self.rows:
            yield sentences


data_train = FetchflowData(args)
preprocessor = SemanticX28Preprocessor(remove_stopwords=False)  # do not remove stopwords for training!
classifier = SemanticClassifier(args.model)

if __name__ == '__main__':
    rows_processed = preprocessor.preprocess(data_train, data_train.num_rows)
    rows = (row.processed for row in rows_processed)
    classifier.train_model(MySentences(rows))
