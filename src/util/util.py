import logging
import re
import sys

import nltk

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def find_str1_in_str2(str1, str2):
    """finds indices of occurences of str1 in str2"""
    return (match.start() for match in re.finditer(re.escape(str1), str2))


def create_contexts(text, word):
    contexts = list()
    str1 = re.sub('\s\s+', ' ', word)
    str2 = re.sub('\s\s+', ' ', text)
    indices = find_str1_in_str2(str1, str2)
    for ix in indices:
        contexts.append('...' + str2[ix - 10:ix + len(word) + 10] + '...')
    return contexts


def flatten(iterable):
    return (item for sublist in iterable for item in sublist)


def create_sentences(contents):
    sentences = (nltk.sent_tokenize(content) for content in contents)
    return flatten(sentences)


def create_words(sentences):
    words = (nltk.word_tokenize(sent, language='german') for sent in sentences)
    return words
    # return flatten(words) # do not flatten as NLTK taggers expect lists of words!
