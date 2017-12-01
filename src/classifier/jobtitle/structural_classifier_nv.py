import itertools
import operator

from src.classifier.jobtitle.structural_classifier import StructuralClassifier

# number of nouns/verbs to use as features (i.e. the top n nouns and the top n features)
# --> size of the featureset will be 2n
n = 5


def top_n(tagged_words, tag, n):
    """returns the n most frequent words with tag {tag} """
    tagged_words_with_tag = (w for (w, t) in tagged_words if t.startswith(tag))
    dct = {k: sum(1 for _ in g) for k, g in itertools.groupby(tagged_words_with_tag)}
    top = sorted(dct.items(), key=operator.itemgetter(1), reverse=True)
    return top[:n]


class StructuralClassifierNV(StructuralClassifier):
    def extract_features(self, tagged_words):
        # convert to list because of two passes!
        tagged_words = list(tagged_words)
        top_n_nouns = top_n(tagged_words, 'N', n)
        top_n_verbs = top_n(tagged_words, 'V', n)
        #
        features = {}
        for i, (noun, count) in enumerate(top_n_nouns, 1):
            features['noun-{}'.format(i)] = noun
        for i, (verb, count) in enumerate(top_n_verbs, 1):
            features['verb-{}'.format(i)] = verb
        return features

    def title(self):
        return 'Structural Classifier (POS-Tags only)'

    def description(self):
        return """Classifies text according to POS tag patterns. Only the plaintext of a vacancy is considered.
        The n most frequent nouns and verbs are extracted as features. 
        """

    def label(self):
        return 'structural_nv'
