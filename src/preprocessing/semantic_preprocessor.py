from src.preprocessing import preproc
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor
from src.util import util


class SemanticPreprocessor(RelevantTagsPreprocessor):
    def __init__(self, data_source, remove_stopwords=False):
        super(SemanticPreprocessor, self).__init__(data_source)
        self.remove_stopwords = remove_stopwords

    def preprocess_single(self, row):
        sentences = util.flatten(preproc.to_sentences(paragraph) for paragraph in row.plaintext.split('\n'))
        word_lists = preproc.sentence_list_to_word_list(sentences)
        word_lists = (list(preproc.remove_punctuation(words)) for words in word_lists)
        if self.remove_stopwords:
            word_lists = (preproc.remove_stop_words(words) for words in word_lists)
        return word_lists
