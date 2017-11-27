import pickle

from src import preproc
from src.preprocessing.create_nltk_pos_tagger_german import german_pos_tagger_path
from src.preprocessing.preprocessor import Preprocessor
from src.util import util

german_pos_tagger = None
with open(german_pos_tagger_path, 'rb') as f:
    german_pos_tagger = pickle.load(f)


def create_pos_tags(words_list, html_tags):
    result = []
    for words, tag in zip(words_list, html_tags):
        tagged_words = german_pos_tagger.tag(words)
        for (content, pos) in tagged_words:
            result.append((content, pos, tag))
    return result


def stem_words(tagged_words):
    return ((preproc.stem(word), tag) for word, tag in tagged_words)


def split_tag_content(html):
    tags = preproc.extract_relevant_tags(html)
    tags_contents = ((tag.name, tag.getText()) for tag in tags)
    return zip(*tags_contents)


def contents_to_sentences(contents):
    for content in contents:
        yield preproc.to_sentences(content)


def extract_words_list(sentences_per_content):
    for sentences in sentences_per_content:
        words_list_per_sentence = [list(preproc.to_words(sentence)) for sentence in sentences]
        words_list = [list(preproc.remove_punctuation(words_list)) for words_list in words_list_per_sentence]
        yield words_list


def extract_pos_tags(words_tokens_list):
    tagged_words_list = (german_pos_tagger.tag(list(word_tokens)) for word_tokens in words_tokens_list)
    for tagged_words in tagged_words_list:
        yield list(pos_tag for (word, pos_tag) in tagged_words)


class StructuralPreprocessorNVT(Preprocessor):
    def __init__(self):
        super(StructuralPreprocessorNVT, self).__init__()

    def preprocess_single(self, row):
        tags, contents = split_tag_content(row.html)
        words_list = extract_words_list(contents)
