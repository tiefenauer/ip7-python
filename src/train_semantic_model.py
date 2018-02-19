import argparse
import logging

from src.classifier.jobtitle.jobtitle_classifier_semantic import JobtitleSemanticClassifier
from src.corpus.corpus_fetchflow_otf import FetchflowOTFCorpus
from src.corpus.x28_corpus_otf import X28OTFCorpus
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

if __name__ == '__main__':
    if args.source == 'fetchflow':
        sentences = FetchflowOTFCorpus(args.id)
        # comment out for on-the-fly-processing
        # sentences = FetchflowCorpus(args.id)
    else:
        sentences = X28OTFCorpus()

    classifier = JobtitleSemanticClassifier(args.model)
    logging.info('Training semantic classifier on {} data'.format(args.source))
    classifier.train_classifier(sentences)
