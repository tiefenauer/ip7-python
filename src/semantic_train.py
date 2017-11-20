import argparse
import logging

import sys

from src import db
from src.classifier.semantic_classifier import SemanticClassifier
from src.database.FetchflowData import FetchflowData
from src.database.X28_Data_Train import X28_Data_Train
from src.db import Database
from src.preprocessing.preprocessor_semantic import SemanticX28Preprocessor

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
parser = argparse.ArgumentParser(description="""Train Semantic Classifier (Word2Vec)""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-l', '--limit', nargs='?', type=float, default=0.8,
                    help='(optional) fraction of labeled data to use for training')
parser.add_argument('-o', '--offset', nargs='?', type=float, default=0.0,
                    help='(optional) fraction value of labeled data to start from')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
args = parser.parse_args()


class MySentences(object):
    def __init__(self, rows):
        self.rows = rows

    def __iter__(self):
        for sentences in self.rows:
            yield sentences


# conn = db.connect_to(Database.X28_PG)
# cursor = conn.cursor()
# cursor.execute("SELECT count(*) AS num_rows FROM fetchflow_html")
# num_rows = cursor.fetchone()['num_rows']
# cursor.execute("SELECT id, fetchflow_id, html FROM fetchflow_html limit 1000")
# data_train = cursor
data_train = FetchflowData(args)
# data_train = X28_Data_Train(args)
preprocessor = SemanticX28Preprocessor(remove_stopwords=False)  # do not remove stopwords for training!
classifier = SemanticClassifier(args.model)

if __name__ == '__main__':
    rows_processed = preprocessor.preprocess(data_train, data_train.num_rows)
    rows = (row.processed for row in rows_processed)
    classifier.train_model(MySentences(rows))
