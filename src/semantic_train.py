import argparse
import logging
import re
import sys

import nltk
from gensim.models import word2vec
from nltk.corpus import stopwords
from tqdm import tqdm

from src import preproc
from src.importer.data_train import TrainingData

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stops = set(stopwords.words('german'))
tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')


def to_sentence(markup, tokenizer, remove_stopwords=False):
    raw_sentences = tokenizer.tokenize(markup.strip())
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(to_wordlist(raw_sentence, remove_stopwords))

    return sentences


def to_wordlist(markup, remove_stopwords=False):
    text = preproc.parse(markup).get_text()
    text = re.sub("[^a-zA-Z]", " ", text)
    words = text.lower().split()
    if remove_stopwords:
        words = [w for w in words if w not in stops]
    return (words)


if __name__ == '__main__':
    logging.info('Preprocessing data...')
    sentences = []
    with TrainingData(args.id) as data_train:
        for row in (row for row in tqdm(data_train, total=data_train.num_rows, unit=' rows') if row['html']):
            sentences += to_sentence(row['html'], tokenizer)

    logging.info('created {} sentences'.format(len(sentences)))
    logging.info('Training Word2Vec model')
    num_features = 300
    min_word_count = 40
    num_workers = 6
    context = 10
    downsampling = 1e-3
    model = word2vec.Word2Vec(sentences,
                              workers=num_workers,
                              size=num_features,
                              min_count=min_word_count,
                              window=context,
                              sample=downsampling
                              )
    model.init_sims()
    model_name = '300features_40minwords_10context'
    model.save(model_name)
