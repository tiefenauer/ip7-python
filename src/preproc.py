import collections
import pickle
import re
import types

import nltk
from bs4 import BeautifulSoup
from lxml import etree
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from src.preprocessing.create_nltk_pos_tagger_german import german_pos_tagger_path
from src.util import html_util
from src.util.html_util import remove_all_attrs, strip_content
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


def extract_relevant_tags(markup):
    soup = parse(markup)
    return (tag for tag in
            (strip_content(tag) for tag in
             (remove_all_attrs(tag) for tag in soup.findAll(html_util.RELEVANT_TAGS))
             )
            if len(tag.getText(strip=True)) > 2
            )


def parse(markup):
    # lxml parser removes the CDATA section!
    return BeautifulSoup(markup, 'lxml')


def remove_html_clutter(soup):
    tags = []
    html_util.extract_tags(soup, tags)
    return tags


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
    return re.sub('([^A-Za-zäöüéèà\/\- ]*)', '', word)


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
