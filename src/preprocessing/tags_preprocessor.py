from bs4 import Comment

from src.preprocessing import preproc
from src.preprocessing.preprocessor import Preprocessor


class TagsPreprocessor(Preprocessor):
    """extracts all tags with readable content, i.e. no script, meta, etc..."""

    def preprocess_single(self, row):
        soup = preproc.parse(row.html)
        [tag.extract() for tag in soup('script')]
        [tag.extract() for tag in soup('noscript')]
        [tag.extract() for tag in soup('meta')]
        [tag.extract() for tag in soup('link')]
        [tag.extract() for tag in soup('style')]
        [tag.extract() for tag in soup('iframe')]
        [tag.extract() for tag in soup('input')]
        [tag.extract() for tag in soup('img')]
        # remove comments
        [tag.extract() for tag in soup.findAll(text=lambda text: isinstance(text, Comment))]
        return soup.findAll()
