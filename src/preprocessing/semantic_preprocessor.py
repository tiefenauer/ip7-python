from src.preprocessing import preproc
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor


class SemanticPreprocessor(RelevantTagsPreprocessor):
    def __init__(self, raw_data, remove_stopwords=False):
        super(SemanticPreprocessor, self).__init__(raw_data)
        self.remove_stopwords = remove_stopwords

    def preprocess_single(self, row):
        sentences = preproc.to_sentences(row.plaintext)
        word_lists = preproc.sentence_list_to_word_list(sentences)
        words = (list(preproc.remove_punctuation(words)) for words in word_lists)
        if self.remove_stopwords:
            words = preproc.remove_stop_words(words)

        return words
