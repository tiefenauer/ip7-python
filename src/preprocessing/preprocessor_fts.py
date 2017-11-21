from src import preproc
from src.preprocessing.x28_preprocessor import X28Preprocessor


class FtsX28Preprocessor(X28Preprocessor):
    def preprocess_single(self, row):
        dom = preproc.parse(row.html)
        relevant_tags = preproc.extract_relevant_tags(dom)
        return set(relevant_tags)
