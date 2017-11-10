from src import preproc
from src.preprocessing.x28_preprocessor import X28Preprocessor


class FtsX28Preprocessor(X28Preprocessor):
    def preprocess_single(self, markup):
        return preproc.preprocess(markup)
