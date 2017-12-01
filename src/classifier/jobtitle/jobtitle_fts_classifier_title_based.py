from src.classifier.jobtitle.jobtitle_fts_classifier import JobtitleFtsClassifier


class TitleBasedJobtitleFtsClassifier(JobtitleFtsClassifier):
    def extract(self, tags):
        title = None
        for tag in (tag for tag in tags if tag.name and tag.name == 'title'):
            title = tag.getText()
        return title

    def title(self):
        return 'Jobtitle Extractor: FTS (title-tag-based)'

    def description(self):
        return """Extracts a jobtitle by only looking at the title tag of a DOM. The title tag is used as extracted
        information."""

    def label(self):
        return 'jobtitle-jobtitle-title'
