import pickle

import nltk

from src import preproc
from src.preprocessing.create_nltk_pos_tagger_german import german_pos_tagger_path
from src.preprocessing.x28_preprocessor import X28Preprocessor
from src.util import util

german_pos_tagger = None
with open(german_pos_tagger_path, 'rb') as f:
    german_pos_tagger = pickle.load(f)


def remove_tags(tags):
    return (tag.get_text() for tag in tags)


def create_sentences(contents):
    sentences = (nltk.sent_tokenize(content) for content in contents)
    return util.flatten(sentences)


def create_words(sentences):
    words = (nltk.word_tokenize(sent, language='german') for sent in sentences)
    return words
    # return flatten(words) # do not flatten as NLTK taggers expect lists of words!


def create_pos_tags(words_list):
    tagged_words = (german_pos_tagger.tag(words) for words in words_list)
    return util.flatten(tagged_words)


def stem_words(tagged_words):
    return ((preproc.stem(word), tag) for word, tag in tagged_words)


class StructuralX28Preprocessor(X28Preprocessor):
    def __init__(self):
        super(X28Preprocessor, self).__init__()

    def preprocess_single(self, markup):
        tags = preproc.extract_relevant_tags(markup)
        contents = remove_tags(tags)
        sentences = create_sentences(contents)
        words = create_words(sentences)
        tagged_words = create_pos_tags(words)
        tagged_stems = stem_words(tagged_words)
        return tagged_stems
