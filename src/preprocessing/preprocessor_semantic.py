import logging
import sys

import nltk
from nltk.corpus import stopwords

from src import preproc
from src.preprocessing.x28_preprocessor import X28Preprocessor

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stops = set(stopwords.words('german'))
tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')


def to_wordlist(markup, remove_stopwords):
    text = preproc.parse(markup).get_text()
    words = preproc.to_words(text)
    words = preproc.remove_punctuation(words)
    if remove_stopwords:
        words = preproc.remove_stop_words(words)
    return words


class SemanticX28Preprocessor(X28Preprocessor):
    def __init__(self, remove_stopwords=False):
        super(X28Preprocessor, self).__init__()
        self.remove_stopwords = remove_stopwords

    def preprocess_single(self, markup):
        raw_sentences = tokenizer.tokenize(markup.strip())
        sentences = []
        for raw_sentence in raw_sentences:
            if len(raw_sentence) > 0:
                sentences += to_wordlist(raw_sentence, self.remove_stopwords)

        return sentences
