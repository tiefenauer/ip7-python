from src.preprocessing import preproc
from src.preprocessing.tags_preprocessor import TagsPreprocessor
from src.util import html_util


class RelevantTagsPreprocessor(TagsPreprocessor):
    """FTS-Preprocessor extracts relevant tags from markup"""

    def preprocess_single(self, row):
        tags = super(RelevantTagsPreprocessor, self).preprocess_single(row)
        tags = (tag for tag in tags if tag.name in html_util.RELEVANT_TAGS)
        tags = (tag for tag in tags if preproc.tag_is_atomic(tag))
        tags = (preproc.remove_strong_and_b_tags(tag) for tag in tags)
        tags = (html_util.remove_all_attrs(tag) for tag in tags)
        tags = (html_util.strip_content(tag) for tag in tags)
        tags = (tag for tag in tags if len(tag.getText()) > 2)

        relevant_tags = []
        seen = set()
        for tag in tags:
            if tag not in seen:
                relevant_tags.append(tag)
                seen.add(tag)
        return relevant_tags
