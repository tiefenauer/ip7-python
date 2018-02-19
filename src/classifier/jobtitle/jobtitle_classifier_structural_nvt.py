import itertools
import operator

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.model_based_classifier import ModelClassifier
from src.util.html_util import calculate_tag_weight


def extract_features(tagged_words):
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


def top_n(tagged_words, pos_tag_prefix, n):
    """returns the n most frequent words with the given POS-Tag-Prefix"""

    words = [(word, html_tag) for (word, pos_tag, html_tag) in tagged_words if pos_tag.startswith(pos_tag_prefix)]
    html_tags_by_word = itertools.groupby(words, operator.itemgetter(0))

    # to dict with highest tag as value
    dct = {}
    for word, group in html_tags_by_word:
        word_count = 0
        for _, html_tag in group:
            word_count += 1
            if word not in dct:
                highest_tag = html_tag
            else:
                highest_tag = dct[word][0]
                if calculate_tag_weight(html_tag) < calculate_tag_weight(highest_tag):
                    highest_tag = html_tag
            dct[word] = (highest_tag, word_count)

    # convert to 3-tuple (word, highest_tag, count)
    items = [(key, value[0], value[1]) for (key, value) in list(dct.items())]
    # sort by highest_tag
    top = sorted(items, key=lambda item: calculate_tag_weight(item[1]))
    # return top n
    return top[:n]


class JobtitleStructuralClassifierNVT(ModelClassifier, JobtitleClassifier):
    """Predicts a job title using the top n nouns and verbs from the processed data as features to train the model.
    Each verb or noun is counted and only the most n frequent words are used. Additionally for each word the HTML tag
    is used as a feature. If a word appears in more than one tag, only the most important tag is used. Tag importance
    is evaluated using an internal list going from 'h1' (more important) to 'p' (less important).
    This means, in order to train the model the preprocessed data must be must be supplied as word tokens together
    with their POS tags and the HTML tags they appear in."""
    count = 0

    def predict_class(self, tagged_word_tokens):
        features = extract_features(tagged_word_tokens)
        result = self.model.classify(features)
        return result

    def title(self):
        return 'Structural Classifier (POS-Tags + HTML Tags)'

    def label(self):
        return 'structural_nvt'
