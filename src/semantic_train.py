import argparse
import logging
import sys

from src.classifier.semantic_classifier import SemanticClassifier
from src.importer.data_train import TrainingData
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

preprocessor = SemanticPreprocessor()
classifier = SemanticClassifier()

if __name__ == '__main__':
    with TrainingData(args.id) as data_train:
        sentences = preprocessor.preprocess(data_train)
        classifier.train(sentences)
