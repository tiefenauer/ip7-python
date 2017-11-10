import re

import nltk
from nltk.corpus import stopwords

from src import preproc
from src.preprocessing.preprocessor import Preprocessor

stops = set(stopwords.words('german'))
tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')


def to_sentence(markup, tokenizer, remove_stopwords=False):
    raw_sentences = tokenizer.tokenize(markup.strip())
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences += to_wordlist(raw_sentence, remove_stopwords)

    return sentences


def to_wordlist(markup, remove_stopwords=False):
    text = preproc.parse(markup).get_text()
    text = re.sub("[^a-zA-Z]", " ", text)
    words = text.lower().split()
    if remove_stopwords:
        words = [w for w in words if w not in stops]
    return words


class SemanticPreprocessor(Preprocessor):
    def preprocess_single(self, markup):
        return to_sentence(markup, tokenizer)
