import logging
import re
import sys

import nltk
from nltk.corpus import stopwords

from src import preproc
from src.preprocessing.x28_preprocessor import X28Preprocessor

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stops = set(stopwords.words('german'))
tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')


def to_wordlist(markup, remove_stopwords=False):
    text = preproc.parse(markup).get_text()
    text = re.sub("[^a-zA-Z]", " ", text)
    words = text.lower().split()
    if remove_stopwords:
        words = [w for w in words if w not in stops]
    return words


class SemanticX28Preprocessor(X28Preprocessor):
    def preprocess_single(self, markup):
        raw_sentences = tokenizer.tokenize(markup.strip())
        sentences = []
        for raw_sentence in raw_sentences:
            if len(raw_sentence) > 0:
                sentences += to_wordlist(raw_sentence, False)

        return sentences
