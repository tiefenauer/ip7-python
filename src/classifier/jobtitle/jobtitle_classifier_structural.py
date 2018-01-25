import gzip
import pickle
import re

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.model_based_classifier import ModelClassifier

special_chars = re.compile('([^A-Za-zäöüéèà]*)')


def extract_nouns(tagged_word_tokens):
    nouns = []
    for noun in (lemma for (lemma, pos, _) in tagged_word_tokens if pos == 'NN'):
        noun = re.sub(special_chars, '', noun)
        if len(noun) > 2:
            nouns.append(noun.strip())
    return ' '.join(nouns)


class JobtitleStructuralClassifier(ModelClassifier, JobtitleClassifier):
    """Classifier to predict job title using structural information from preprocessed data. Structural data usually
    consists of the tokenized words and some additional information about the inner structure of the text.
    A Naive Bayes classifier is trained to make predictions about the job title for unkown instances.
    """

    count = 0

    def __init__(self, model, vectorizer):
        super(JobtitleStructuralClassifier, self).__init__(model)
        self.vectorizer = vectorizer

    def predict_class(self, tagged_word_tokens):
        nouns = extract_nouns(tagged_word_tokens)
        X = self.vectorizer.transform([nouns])
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
