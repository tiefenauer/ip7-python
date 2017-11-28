from src import preproc
from src.preprocessing.preprocessor import Preprocessor


class SemanticPreprocessor(Preprocessor):
    def __init__(self, remove_stopwords=False):
        super(Preprocessor, self).__init__()
        self.remove_stopwords = remove_stopwords

    def preprocess_single(self, row):
        words = preproc.to_words(row.plaintext)
        words = preproc.remove_punctuation(words)
        if self.remove_stopwords:
            words = preproc.remove_stop_words(words)

        return words
