from src import preproc
from src.preprocessing.preprocessor import Preprocessor
from src.util import util


class StructuralPreprocessorNV(Preprocessor):
    def __init__(self):
        super(StructuralPreprocessorNV, self).__init__()

    def preprocess_single(self, row):
        sentences = preproc.to_sentences(row.plaintext)
        words_lists = preproc.sentence_list_to_word_list(sentences)
        words_lists = (preproc.remove_punctuation(word_list) for word_list in words_lists)
        tagged_words = preproc.pos_tag(words_lists)
        tagged_words = util.flatten(tagged_words)
        tagged_stems = ((preproc.stem(word), tag) for word, tag in tagged_words)
        return tagged_stems
