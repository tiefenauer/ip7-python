import argparse

from src.classifier.jobtitle.jobtitle_classifier_structural import JobtitleStructuralClassifier
from src.database.train_data_x28 import X28TrainData
from src.util.log_util import log_setup

parser = argparse.ArgumentParser(description="""Train Structural Classifier (NLTK)""")
parser.add_argument('source', nargs='?', choices=['fetchflow', 'x28'], default='fetchflow')
parser.add_argument('id', nargs='?', type=int)
parser.add_argument('-s', '--split', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
args = parser.parse_args()

logging = log_setup()

data_train = X28TrainData(args)
classifier = JobtitleStructuralClassifier(args)

if __name__ == '__main__':
    classifier.train_classifier(data_train)
