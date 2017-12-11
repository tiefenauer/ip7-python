from src.preprocessing import preproc
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor


class LoePreprocessor(RelevantTagsPreprocessor):

    def preprocess_single(self, row):
        title_tag = preproc.create_tag('title', row.title)
        relevant_tags = super(LoePreprocessor, self).preprocess_single(row)
        relevant_tags.add(title_tag)
        return relevant_tags
