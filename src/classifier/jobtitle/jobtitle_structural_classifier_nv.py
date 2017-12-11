import itertools
import operator

from src.classifier.jobtitle.jobtitle_structural_classifier import JobtitleStructuralClassifier
# number of nouns/verbs to use as features (i.e. the top n nouns and the top n features)
# --> size of the featureset will be 2n
from src.preprocessing.structural_preprocessor_nv import StructuralPreprocessorNV

n = 5


def top_n(tagged_words, tag, n):
    """returns the n most frequent words with tag {tag} """
    tagged_words_with_tag = (w for (w, t) in tagged_words if t.startswith(tag))
    dct = {k: sum(1 for _ in g) for k, g in itertools.groupby(tagged_words_with_tag)}
    top = sorted(dct.items(), key=operator.itemgetter(1), reverse=True)
    return top[:n]


class JobtitleStructuralClassifierNV(JobtitleStructuralClassifier):
    """Predicts a job title using the top n nouns and verbs from the processed data as features to train the model.
    Each verb or noun is counted and only the most n frequent words are used. No other information is used.
    This means, in order to train the model the preprocessed data must be must be supplied as word tokens together
    with their POS."""

    def __init__(self, args, preprocessor=StructuralPreprocessorNV):
        super(JobtitleStructuralClassifierNV, self).__init__(args, preprocessor)

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

    def label(self):
        return 'structural_nv'
