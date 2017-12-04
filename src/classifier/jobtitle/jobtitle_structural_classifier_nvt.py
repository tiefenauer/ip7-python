import itertools
import operator

from src.classifier.jobtitle.jobtitle_structural_classifier import JobtitleStructuralClassifier
from src.preprocessing.structural_preprocessor_nvt import StructuralPreprocessorNVT

html_tags = ['h1', 'h2', 'h3', 'h4']


def compare_tag(t1, t2):
    """return numeric value of tags for comparison"""
    i1 = html_tags.index(t1) if t1 in html_tags else 1000
    i2 = html_tags.index(t2) if t2 in html_tags else 1000
    return i1 - i2


def get_higher_tag(t1, t2):
    """compare 2 tags and return higher ranked tag"""
    i = compare_tag(t1, t2)
    if i < 0:
        return t1
    if i > 0:
        return t2
    return t1


def top_n(tagged_words, pos_tag, n):
    """returns the n most frequent words with tag {tag} """
    words_with_pos_tag = [(word, htag) for (word, ptag, htag) in tagged_words
                          if ptag.startswith(pos_tag)]

    # group by word
    words_grouped = itertools.groupby(words_with_pos_tag, operator.itemgetter(0))
    # to dict with highest tag as value
    dct = {}
    for word, group in words_grouped:
        word_count = 0
        for _, html_tag in group:
            word_count += 1
            if word not in dct:
                highest_tag = html_tag
            else:
                highest_tag = get_higher_tag(dct[word][0], html_tag)
            dct[word] = (highest_tag, word_count)

    # convert to 3-tuple (word, highest_tag, count)
    items = [(key, value[0], value[1]) for (key, value) in list(dct.items())]
    # sort by highest_tag
    top = sorted(items, key=lambda item: html_tags.index(item[1]) if item[1] in html_tags else 1000)
    # return top n
    return top[:n]


class JobtitleStructuralClassifierNVT(JobtitleStructuralClassifier):
    def __init__(self, args):
        preprocessor = StructuralPreprocessorNVT()
        super(JobtitleStructuralClassifierNVT, self).__init__(args, preprocessor)

    def extract_features(self, tagged_words):
        # convert to list because of two passes!
        tagged_words = list(tagged_words)
        top_n_nouns = top_n(tagged_words, 'N', 5)
        top_n_verbs = top_n(tagged_words, 'V', 5)

        # create features
        features = {}
        for i, (noun, highest_tag, count) in enumerate(top_n_nouns, 1):
            features['N-word-{}'.format(i)] = noun
            features['N-tag-{}'.format(i)] = highest_tag
        for i, (verb, highest_tag, count) in enumerate(top_n_verbs, 1):
            features['V-word-{}'.format(i)] = verb
            features['V-tag-{}'.format(i)] = highest_tag
        return features

    def title(self):
        return 'Structural Classifier (POS-Tags + HTML Tags)'

    def label(self):
        return 'structural_nvt'

    def description(self):
        return """Classifies text according to POS tag patterns and HTML tags. HTML tags are used as features.
        The n most frequent nouns and verbs are extracted as features. 
        """
