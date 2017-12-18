from bs4 import Comment

from src.preprocessing import preproc
from src.preprocessing.preprocessor import Preprocessor

NON_HUMAN_READABLE_TAGS = ['script', 'noscript', 'meta', 'link', 'style', 'iframe', 'input', 'img']


class HTMLPreprocessor(Preprocessor):
    """parses markup as HTML and extracts all tags with human readable content, i.e. no script, meta, etc..."""

    def preprocess_single(self, row):
        soup = preproc.parse(row.html)
        [tag.extract() for tag in soup.findAll() if tag.name in NON_HUMAN_READABLE_TAGS]
        [tag.extract() for tag in soup.findAll(text=lambda text: isinstance(text, Comment))]
        return (tag for tag in soup.findAll())
