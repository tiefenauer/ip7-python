from src.preprocessing.preprocessor import Preprocessor


class PlaintextPreprocessor(Preprocessor):

    def preprocess_single(self, row):
        return row.plaintext