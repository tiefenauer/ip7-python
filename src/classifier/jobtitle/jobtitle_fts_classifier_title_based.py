from src.classifier.fts_classifier import FtsClassifier
from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier


class TitleBasedJobtitleFtsClassifier(FtsClassifier, JobtitleClassifier):
    """Extracts a jobtitle by only looking at the title tag of a DOM. The title tag is used as extracted information."""

    def classify(self, tags):
        title = None
        for tag in (tag for tag in tags if tag.name and tag.name == 'title'):
            title = tag.getText()
        return title

    def title(self):
        return 'Jobtitle Extractor: FTS (title-tag-based)'

    def label(self):
        return 'jobtitle-fts-title'
