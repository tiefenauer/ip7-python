from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.tag_classifier import TagClassifier


class TitleBasedJobtitleFtsClassifier(TagClassifier, JobtitleClassifier):
    """Extracts a jobtitle by only looking at the title tag of a DOM. The title tag is used as extracted information."""

    def predict_class(self, tags):
        title = None
        for tag in (tag for tag in tags if tag.name and tag.name == 'title'):
            title = tag.getText()
        return title

    def title(self):
        return 'Jobtitle Classifier: FTS (title-tag-based)'

    def label(self):
        return 'jobtitle-fts-title'
