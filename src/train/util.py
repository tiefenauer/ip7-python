import collections
import re


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


def flatten(it):
    for x in it:
        if (isinstance(x, collections.Iterable) and
                not isinstance(x, str)):
            yield from flatten(x)
        else:
            yield x