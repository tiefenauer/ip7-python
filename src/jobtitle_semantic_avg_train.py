import argparse
import logging
import os

from tqdm import tqdm

from src.classifier.jobtitle.jobtitle_semantic_classifier_avg import JobtitleSemanticClassifierAvg
from src.database.X28TrainData import X28TrainData
from src.database.fetchflow_dat import FetchflowData
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Train Semantic Classifier (Word2Vec)""")
parser.add_argument('source', nargs='?', choices=['fetchflow', 'x28'], default='fetchflow')
parser.add_argument('-s', '--split', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
args = parser.parse_args()

relevant_tags_preprocessor = RelevantTagsPreprocessor(include_title=False)
semantic_preprocessor = SemanticPreprocessor()


class FetchflowCorpus(object):
    """creates sentences from preprocessed corpus file"""

    def __init__(self):
        self.dirname = 'D:/db/'

    def __iter__(self):
        with open(os.path.join(self.dirname, 'fetchflowcorpus'), encoding='utf-8') as corpus:
            for line in corpus:
                yield line.split()


class FetchflowOTFCorpus(object):
    """creates sentences on the fly by preprocessing Fetchflow rows from DB"""

    def __iter__(self):
        class DummyRow(object):
            def __init__(self, html):
                self.html = html
                self.plaintext = None

        fetchflow_rows = FetchflowData(args)
        for fetchflow_row in tqdm(fetchflow_rows, unit=' rows'):
            row = DummyRow(html=fetchflow_row.html)
            tags = relevant_tags_preprocessor.preprocess_single(row)
            plaintext = '\n'.join(tag.getText() for tag in tags)
            row.plaintext = plaintext
            for sentence in semantic_preprocessor.preprocess_single(row):
                if len(sentence) > 1:
                    yield sentence


class X28Corpus(object):
    def __iter__(self):
        for row, sentences in SemanticPreprocessor(X28TrainData(args)):
            for sent in sentences:
                yield sent


if __name__ == '__main__':
    if args.source == 'fetchflow':
        sentences = FetchflowOTFCorpus()
        # comment out for on-the-fly-processing
        sentences = FetchflowCorpus()
    else:
        sentences = X28Corpus()

    classifier = JobtitleSemanticClassifierAvg(args.model)
    logging.info('Training semantic classifier on {} data'.format(args.source))
    classifier.train_classifier(sentences)
