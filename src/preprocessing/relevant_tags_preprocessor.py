from src.preprocessing import preproc
from src.preprocessing.html_preprocessor import HTMLPreprocessor
from src.util import html_util


class RelevantTagsPreprocessor(HTMLPreprocessor):
    """FTS-Preprocessor extracts relevant tags from markup"""

    def preprocess_single(self, row):
        tags = super(RelevantTagsPreprocessor, self).preprocess_single(row)
        tags = (tag for tag in tags if html_util.is_relevant(tag))
        tags = (tag for tag in tags if preproc.tag_is_atomic(tag))
        tags = (preproc.remove_strong_and_b_tags(tag) for tag in tags)
        tags = (html_util.remove_all_attrs(tag) for tag in tags)
        tags = (html_util.strip_content(tag) for tag in tags)
        tags = (tag for tag in tags if len(tag.getText()) > 2)

        relevant_tags = []
        seen = set()
        for tag in tags:
            text = tag.getText()
            if text not in seen:
                relevant_tags.append(tag)
                seen.add(text)
        return relevant_tags
