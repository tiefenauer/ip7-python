from src import preproc
from src.preprocessing.x28_preprocessor import X28Preprocessor


class SemanticX28Preprocessor(X28Preprocessor):
    def __init__(self, remove_stopwords=False):
        super(X28Preprocessor, self).__init__()
        self.remove_stopwords = remove_stopwords

    def preprocess_single(self, row):
        words = preproc.to_words(row.plaintext)
        words = preproc.remove_punctuation(words)
        if self.remove_stopwords:
            words = preproc.remove_stop_words(words)

        return words
