from src import preproc
from src.preprocessing.x28_preprocessor import X28Preprocessor


class FtsX28Preprocessor(X28Preprocessor):
    def preprocess_single(self, dom):
        dom = preproc.parse(dom)
        relevant_tags = preproc.extract_relevant_tags(dom)
        return set(relevant_tags)
