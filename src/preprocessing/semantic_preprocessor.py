from src.preprocessing import preproc
from src.preprocessing.preprocessor import Preprocessor


class SemanticPreprocessor(Preprocessor):
    def __init__(self, raw_data, remove_stopwords=False):
        super(SemanticPreprocessor, self).__init__(raw_data)
        self.remove_stopwords = remove_stopwords

    def preprocess_single(self, row):
        # X28-Data has an attribute 'plaintext'
        if hasattr(row, 'plaintext'):
            words = preproc.to_words(row.plaintext)
        # Fetchflow Data needs to be reduced to relevant tags and then the words need to be extracted from there
        else:
            relevant_tags = preproc.extract_relevant_tags(row.html)
            words = preproc.to_words(' '.join(tag.getText() for tag in relevant_tags))
        words = preproc.remove_punctuation(words)
        if self.remove_stopwords:
            words = preproc.remove_stop_words(words)

        return words
