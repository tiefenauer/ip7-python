import argparse

from src.classifier.semantic_classifier_avg import SemanticClassifierAvg
from src.database.FetchflowTrainData import FetchflowTrainData
from src.database.X28TrainData import X28TrainData
from src.util.boot_util import log_setup

log_setup()
parser = argparse.ArgumentParser(description="""Train Semantic Classifier (Word2Vec)""")
parser.add_argument('source', nargs='?', choices=['fetchflow', 'x28'], default='fetchflow')
parser.add_argument('-s', '--split', nargs='?', type=float, default=1.0,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
args = parser.parse_args()

data_train = FetchflowTrainData(args)
if args.source == 'x28':
    data_train = X28TrainData(args)

classifier = SemanticClassifierAvg(args.model)

if __name__ == '__main__':
    classifier.train_model(data_train)
