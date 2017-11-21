import pickle

from src import preproc
from src.preprocessing.create_nltk_pos_tagger_german import german_pos_tagger_path
from src.preprocessing.x28_preprocessor import X28Preprocessor
from src.util import util, html_util

german_pos_tagger = None
with open(german_pos_tagger_path, 'rb') as f:
    german_pos_tagger = pickle.load(f)


def create_pos_tags(words_list):
    tagged_words = (german_pos_tagger.tag(words) for words in words_list)
    return util.flatten(tagged_words)


def stem_words(tagged_words):
    return ((preproc.stem(word), tag) for word, tag in tagged_words)


class StructuralX28Preprocessor(X28Preprocessor):
    def __init__(self):
        super(X28Preprocessor, self).__init__()

    def preprocess_single(self, row):
        sentences = preproc.to_sentences(row.plaintext)
        words = preproc.sentence_list_to_word_list(sentences)
        tagged_words = create_pos_tags(words)
        tagged_stems = stem_words(tagged_words)
        return tagged_stems
