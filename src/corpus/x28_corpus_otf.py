from src.database.train_data_x28 import X28TrainData
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor


class X28OTFCorpus(object):
    def __init__(self, corpus_data=X28TrainData()):
        self.corpus_data = corpus_data

    def __iter__(self):
        for row, sentences in SemanticPreprocessor(self.corpus_data):
            for sent in sentences:
                yield sent
