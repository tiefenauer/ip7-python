from src.preprocessing import preproc
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor


class SentencePreprocessor(RelevantTagsPreprocessor):

    def preprocess_single(self, row):
        relevant_tags = super(SentencePreprocessor, self).preprocess_single(row)
        for tag in relevant_tags:
            sentences = preproc.to_sentences(tag.getText())
            for sent in sentences:
                yield tag.name, sent
