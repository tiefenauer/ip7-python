import logging
import sys

from src import preproc
from src.preprocessing.x28_preprocessor import X28Preprocessor
from src.util import html_util, util

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class SemanticX28Preprocessor(X28Preprocessor):
    def __init__(self, remove_stopwords=False):
        super(X28Preprocessor, self).__init__()
        self.remove_stopwords = remove_stopwords

    def preprocess_single(self, markup):
        tags = preproc.extract_relevant_tags(markup)
        contents = html_util.remove_tags(tags)
        sentences = preproc.text_list_to_sentence_list(contents)
        words = preproc.sentence_list_to_word_list(sentences)
        words = util.flatten(words)
        words = preproc.remove_punctuation(words)
        if self.remove_stopwords:
            words = preproc.remove_stop_words(words)

        return words
