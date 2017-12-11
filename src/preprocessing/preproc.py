import collections
import pickle
import re
import types

import nltk
from bs4 import BeautifulSoup, NavigableString
from lxml import etree
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from src.dataimport.create_nltk_pos_tagger_german import german_pos_tagger_path
from src.util.util import flatten

# german POS tagger
with open(german_pos_tagger_path, 'rb') as f:
    german_pos_tagger = pickle.load(f)

stopwords_de = set(stopwords.words('german'))
stemmer = SnowballStemmer('german', ignore_stopwords=True)
xml_parser = etree.HTMLParser(strip_cdata=False)
punctuation_tokens = ['.', '..', '...', ',', ';', ':', '(', ')', '"', '\'', '[', ']',
                      '{', '}', '?', '!', '-', '–', '+', '*', '--', '\'\'', '``']
punctuation = '?.!/;:()&+'

special_chars_pattern = re.compile('([^A-Za-zäöüéèà\/\- ]*)')


def tag_is_atomic(tag):
    children = get_children(tag)
    # only child is string
    if len(children) == 0 or contains_only_strings(children):
        return True
    # tag contains only <strong> or <b> as children
    elif contains_only_semantic_markup(children):
        return True
    # tag is nested
    return False


def get_children(tag):
    children = []
    if hasattr(tag, 'children'):
        children = list(tag.children)
    return children


def contains_only_strings(children):
    return len(children) == 1 and isinstance(children[0], NavigableString)


def contains_only_semantic_markup(children):
    return len(children) == 0 \
           or all(isinstance(child, NavigableString) or child.name in ['strong', 'b', 'br'] for child in children)


def remove_strong_and_b_tags(tag):
    if contains_only_semantic_markup(tag):
        stripped = tag.getText(strip=True, separator=' ')
        if len(stripped) > 0:
            tag.string = stripped
    return tag


def parse(markup):
    # lxml parser removes the CDATA section!
    return BeautifulSoup(markup, 'lxml')


def create_tag(tag_name, tag_content):
    tag = BeautifulSoup('', 'html.parser').new_tag(tag_name)
    if tag_content:
        tag.string = tag_content
    return tag


def create_tags(param):
    return [create_tag(tag_name, tag_content) for (tag_name, tag_content) in param]


def create_tag_from_markup(markup):
    soup = BeautifulSoup(markup, 'html.parser')
    return list(soup.children)[0]


def text_list_to_sentence_list(contents):
    sentences = (to_sentences(content) for content in contents)
    return flatten(sentences)


def sentence_list_to_word_list(sentences):
    words = (to_words(sent) for sent in sentences)
    return words


def to_words(text):
    return nltk.word_tokenize(text, language='german')


def to_sentences(text):
    return nltk.sent_tokenize(text, language='german')


def remove_special_chars(text):
    if is_iterable_and_not_string(text):
        return (remove_special_chars(word) for word in text if len(word) > 0)
    return ' '.join(word for word in (_replace_special_chars(w) for w in text.split(' ')) if len(word) > 0)


def _replace_special_chars(word):
    return re.sub(special_chars_pattern, '', word)


def remove_stop_words(text):
    if isinstance(text, str):
        return ' '.join([word for word in text.split(' ') if word not in stopwords_de])
    return (word for word in text if word not in stopwords_de)


def stem(text):
    """stem a text string or a list of strings"""
    if is_iterable_and_not_string(text):
        return (stem_word(word) for word in text)
    return ' '.join(stem_word(word) for word in text.split(' '))


def stem_word(word):
    """stem a single word string"""
    return stemmer.stem(word)


def pos_tag(word_list):
    if is_generator(word_list):
        return (german_pos_tagger.tag(list(words)) for words in word_list)
    if is_nested_list(word_list):
        return (german_pos_tagger.tag(words) for words in word_list)
    return german_pos_tagger.tag(word_list)


def is_iterable_and_not_string(text):
    return isinstance(text, collections.Iterable) and not isinstance(text, str)


def is_generator(obj):
    return isinstance(obj, types.GeneratorType)


def is_nested_list(lst):
    if is_generator(lst):
        return False
    return any(isinstance(i, list) for i in lst)


def remove_punctuation(words):
    return (word for word in words if word not in punctuation_tokens)
