import argparse
import logging
import sys

from src.classifier.semantic_classifier import SemanticClassifier
from src.importer.data_train import TrainingData
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-l', '--limit', nargs='?', type=float, default=1.0,
                    help='(optional) fraction of base data to use (start value)')
parser.add_argument('-o', '--offset', nargs='?', type=float, default=0.0,
                    help='(optional) fraction of base data to use (end value)')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

preprocessor = SemanticPreprocessor()
classifier = SemanticClassifier(args.model)

if __name__ == '__main__':
    with TrainingData(args.id, args.limit, args.offset) as data_train:
        sentences = preprocessor.preprocess(data_train)
        classifier.train_model(sentences)
