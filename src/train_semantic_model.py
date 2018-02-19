"""
Train a Word2Vec-Model to use in the semantic approach
"""
import argparse
import gzip
import logging
import os
import pickle
import shutil

from gensim.models import word2vec

from src.corpus.corpus_fetchflow_otf import FetchflowOTFCorpus
from src.corpus.x28_corpus_otf import X28OTFCorpus
from src.util.globals import MODELS_DIR
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Train Semantic Classifier (Word2Vec)""")
parser.add_argument('source', nargs='?', choices=['fetchflow', 'x28'], default='fetchflow')
args = parser.parse_args()

model_path = os.path.join(MODELS_DIR, 'semantic.w2v')
model_path_gzip = os.path.join(MODELS_DIR, 'semantic.w2v.gzip')


def train_w2v_model(sentences, num_features=300, min_word_count=20, context=10, num_workers=6, downsampling=1e-3):
    if os.path.exists(model_path):
        log.info('Loading Word2Vec model from {}'.format(model_path))
        return pickle.load(open(model_path, 'rb'))

    log.info('Training new Word2Vec model...')
    model = word2vec.Word2Vec(sentences,
                              workers=num_workers,
                              size=num_features,
                              min_count=min_word_count,
                              window=context,
                              sample=downsampling
                              )
    model.init_sims()

    log.info('compressing and saving model to {}'.format(model_path))
    model.wv.save_word2vec_format(model_path, binary=True)
    with open(model_path, 'rb') as f_in, gzip.open(model_path_gzip, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(model_path)
    log.info('...done!')
    return model_path_gzip


if __name__ == '__main__':
    if args.source == 'fetchflow':
        corpus = FetchflowOTFCorpus()
        # comment out for on-the-fly-processing
        # sentences = FetchflowCorpus(args.id)
    else:
        corpus = X28OTFCorpus()

    logging.info('Training Word2Vec model on {} data'.format(args.source))
    train_w2v_model(corpus)
