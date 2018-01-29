import gzip
import pickle
import re

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.model_based_classifier import ModelClassifier
from src.preprocessing import preproc
from src.util import util

special_chars = re.compile('([^A-Za-zäöüéèà]*)')


def extract_nouns_and_verbs_from_row(row):
    content = '. '.join([row.title, row.plaintext])

    sents = preproc.to_sentences(content)
    words = [preproc.to_words(sent) for sent in sents]
    words = [list(preproc.remove_punctuation(word_list)) for word_list in words]
    pos_words = (preproc.pos_tag(word_list) for word_list in words)

    nouns, verbs = extract_nouns_and_verbs_from_tagged_words(pos_words)

    return ' '.join(nouns), ' '.join(verbs)


def extract_nouns_and_verbs_from_tagged_words(pos_words):
    nouns = []
    verbs = []
    for word, pos in ((word, pos) for (word, pos) in util.flatten(pos_words) if pos[:1] in ['N', 'F', 'V']):
        word = re.sub(special_chars, '', word)
        if len(word) <= 2:
            continue
        word = preproc.lemmatize_word(word, pos)
        if pos == 'NN' or pos.startswith('F'):
            nouns.append(word)
        if pos.startswith('V'):
            verbs.append(word)
    return nouns, verbs


class JobtitleStructuralClassifier(ModelClassifier, JobtitleClassifier):
    """Classifier to predict job title using structural information from preprocessed data. Structural data usually
    consists of the tokenized words and some additional information about the inner structure of the text.
    A Naive Bayes classifier is trained to make predictions about the job title for unkown instances.
    """

    count = 0

    def __init__(self, model, vectorizer):
        super(JobtitleStructuralClassifier, self).__init__(model)
        self.vectorizer = vectorizer

    def predict_class(self, plaintext):
        # nouns, verbs = extract_nouns_and_verbs_from_row(row)
        # result = self.model.predict([nouns + ' ' + verbs])
        X = self.vectorizer.transform([plaintext])
        result = self.model.predict(X)
        return result[0] if result else 'unknown'

    def train_model(self, labeled_data):
        pass

    def serialize_model(self, model, path):
        with open(path, 'wb') as f:
            pickle.dump(model, f)
        return path

    def deserialize_model(self, path):
        model = None
        with gzip.open(path, 'rb') as f:
            model = pickle.load(f)
        return model

    def get_filename_postfix(self):
        return '{}rows'.format(self.count)

    def title(self):
        return 'Structural Classifier (POS-Tags + HTML Tags)'

    def label(self):
        return 'structural'
