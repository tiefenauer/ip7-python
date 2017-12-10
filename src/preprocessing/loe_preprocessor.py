from src.preprocessing import preproc
from src.preprocessing.fts_preprocessor import FtsPreprocessor


class LoePreprocessor(FtsPreprocessor):

    def preprocess_single(self, row):
        title_tag = preproc.create_tag('title', row.title)
        relevant_tags = super(LoePreprocessor, self).preprocess_single(row)
        relevant_tags.add(title_tag)
        return relevant_tags
