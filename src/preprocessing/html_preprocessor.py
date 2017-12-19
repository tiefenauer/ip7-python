import collections

from bs4 import Comment

from src.preprocessing import preproc
from src.preprocessing.preprocessor import Preprocessor

NON_HUMAN_READABLE_TAGS = ['script', 'noscript', 'meta', 'link', 'style', 'iframe', 'input', 'img']


class HTMLPreprocessor(Preprocessor):
    """parses markup as HTML and extracts all tags with human readable content, i.e. no script, meta, etc..."""

    def __init__(self, data_source=None, include_title=True):
        super(HTMLPreprocessor, self).__init__(data_source)
        self.include_title = include_title

    def preprocess_single(self, row):
        soup = preproc.parse(row.html)
        title_tag = preproc.create_tag('title', row.title)
        # remove tags that are not visible to humans
        [tag.extract() for tag in soup.findAll() if tag.name in NON_HUMAN_READABLE_TAGS]
        # remove comments
        [tag.extract() for tag in soup.findAll(text=lambda text: isinstance(text, Comment))]
        all_tags = collections.deque(soup.findAll())
        if self.include_title:
            all_tags.appendleft(title_tag)
        return (tag for tag in all_tags)
