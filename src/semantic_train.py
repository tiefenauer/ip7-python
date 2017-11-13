import argparse
import logging
import sys

from src.classifier.semantic_classifier import SemanticClassifier
from src.importer.data_train import TrainingData
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

if __name__ == '__main__':
    with TrainingData(args) as data_train:
        sentences = list(sentence for (row_id, target_class, sentence) in preprocessor.preprocess(data_train))
        classifier.train_model(sentences)
