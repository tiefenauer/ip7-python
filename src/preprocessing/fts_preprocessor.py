from src import preproc
from src.preprocessing.preprocessor import Preprocessor


class FtsPreprocessor(Preprocessor):
    def preprocess_single(self, row):
        dom = preproc.parse(row.html)
        relevant_tags = preproc.extract_relevant_tags(dom)
        return set(relevant_tags)
