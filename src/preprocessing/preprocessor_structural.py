import pickle

import nltk

from src import preproc
from src.preprocessing.create_nltk_pos_tagger_german import german_pos_tagger_path
from src.preprocessing.x28_preprocessor import X28Preprocessor

german_pos_tagger = None
with open(german_pos_tagger_path, 'rb') as f:
    german_pos_tagger = pickle.load(f)


def remove_tags(tags):
    return (tag.get_text() for tag in tags)


def create_sentences(contents):
    sentences = (nltk.sent_tokenize(content) for content in contents)
    return flatten(sentences)


def create_tags_from_sentences(sentences):
    return (german_pos_tagger.tag(words) for words in (sent.split(' ') for sent in sentences))


def create_words(sentences):
    words = (nltk.word_tokenize(sent, language='german') for sent in sentences)
    return words
    # return flatten(words)


def create_tagged_words(words):
    return (nltk.pos_tag(word, lang='deu') for word in words)


def flatten(some_list):
    return (item for sublist in some_list for item in sublist)


class StructuralX28Preprocessor(X28Preprocessor):
    def __init__(self):
        super(X28Preprocessor, self).__init__()

    def preprocess_single(self, markup):
        tags = preproc.extract_relevant_tags(markup)
        contents = remove_tags(tags)
        sentences = create_sentences(contents)
        tagged_words = create_tags_from_sentences(sentences)
        words = create_words(sentences)
        tagged_words = create_tagged_words(words)
        return sentences
