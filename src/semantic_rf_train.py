import argparse

from src.classifier.semantic_classifier_rf import SemanticClassifierRF
from src.database.X28TrainData import X28TrainData
from src.util.log_util import log_setup

log_setup()

parser = argparse.ArgumentParser(description="""Train Semantic Classifier (Word2Vec)""")
parser.add_argument('source', nargs='?', choices=['fetchflow', 'x28'], default='fetchflow')
parser.add_argument('-s', '--split', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
parser.add_argument('-w2v', '--w2vmodel',
                    help='(optional) pre-trained W2V-Model to use to create RandomForest')
args = parser.parse_args()

if not args.w2vmodel:
    args.w2vmodel = 'semantic_avg_2017-11-23-17-08-20_300features_40minwords_10context.gz'

data_train = X28TrainData(args)
classifier = SemanticClassifierRF(args)
if __name__ == '__main__':
    classifier.train_model(data_train)
