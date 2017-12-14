import argparse

from src.classifier.jobtitle.jobtitle_semantic_classifier_avg import JobtitleSemanticClassifierAvg
from src.database.X28TrainData import X28TrainData
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor
from src.util.log_util import log_setup

log_setup()
parser = argparse.ArgumentParser(description="""Train Semantic Classifier (Word2Vec)""")
parser.add_argument('source', nargs='?', choices=['fetchflow', 'x28'], default='fetchflow')
parser.add_argument('-s', '--split', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
args = parser.parse_args()


class FetchflowCorpus(object):
    def __init__(self):
        self.dirname = 'D:/db/'

    def __iter__(self):
        with open(os.path.join(self.dirname, 'fetchflowcorpus'), encoding='utf-8') as corpus:
            for line in corpus:
                yield line.split()


sentences = SemanticPreprocessor(X28TrainData(args))
if args.source == 'fetchflow':
    # sentences = SemanticPreprocessor(FetchflowTrainData(args))
    sentences = FetchflowCorpus()

classifier = JobtitleSemanticClassifierAvg(args.model)

if __name__ == '__main__':
    classifier.train_classifier(sentences)
