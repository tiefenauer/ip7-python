import collections
import re

import nltk
from bs4 import BeautifulSoup
from lxml import etree
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from src.util import html_util
from src.util.html_util import remove_all_attrs, strip_content
from src.util.util import flatten

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
    sentences = (nltk.sent_tokenize(content) for content in contents)
    return flatten(sentences)


def sentence_list_to_word_list(sentences):
    words = (to_words(sent) for sent in sentences)
    return words


def to_words(text):
    return nltk.word_tokenize(text, language='german')


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
    if is_iterable_and_not_string(text):
        return (stem_word(word) for word in text)
    return ' '.join(stem_word(word) for word in text.split(' '))


def stem_word(word):
    return stemmer.stem(word)


def is_iterable_and_not_string(text):
    return isinstance(text, collections.Iterable) and not isinstance(text, str)


def remove_punctuation(words):
    words = [x for x in words if x not in punctuation_tokens]
    # words = [re.sub('[{}]'.format(punctuation), ' ', x) for x in words]
    return words
