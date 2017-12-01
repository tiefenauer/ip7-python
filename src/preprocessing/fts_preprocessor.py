from src import preproc
from src.preprocessing.preprocessor import Preprocessor


class FtsPreprocessor(Preprocessor):
    def preprocess_single(self, row):
        relevant_tags = preproc.extract_relevant_tags(row.html)
        return set(relevant_tags)
