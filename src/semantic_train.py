import argparse
import logging
import sys

from pony.orm import db_session
from tqdm import tqdm

from src import db
from src.database.FetchflowData import Row
from src.db import Database
from src.classifier.semantic_classifier import SemanticClassifier
from src.database.entities_mysql_fetchflow import Labeled_Text
from src.preprocessing.preprocessor_semantic import SemanticX28Preprocessor

parser = argparse.ArgumentParser(description="""Train Semantic Classifier (Word2Vec)""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-l', '--limit', nargs='?', type=float, default=0.8,
                    help='(optional) fraction of labeled data to use for training')
parser.add_argument('-o', '--offset', nargs='?', type=float, default=0.0,
                    help='(optional) fraction value of labeled data to start from')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

preprocessor = SemanticX28Preprocessor(remove_stopwords=False)  # do not remove stopwords for training!
classifier = SemanticClassifier(args.model)
args.limit = 0.01


class MySentences(object):
    def __init__(self, sentences):
        self.sentences = sentences

    def __iter__(self):
        for sent in self.sentences:
            yield sent


class Bla(object):
    @db_session
    def __init__(self, args):
        self.id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        self.num_rows = Labeled_Text.select(lambda d: self.id < 0 or d.id == self.id).count()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @db_session
    def __iter__(self):
        conn = db.connect_to(Database.FETCHFLOW_MYSQL)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT id, title, CONVERT(contentbytes USING utf8) AS html FROM labeled_text""")
        for row in cursor:
            yield Row(row)


if __name__ == '__main__':
    with Bla(args) as data_train:
        sentences = tqdm(MySentences((row.processed for row in preprocessor.preprocess(data_train))),total=data_train.num_rows)
        classifier.train_model(sentences)
