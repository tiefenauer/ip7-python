from src.classifier.fts_classifier import FtsClassifier


class TitleBasedJobTitleClassifier(FtsClassifier):
    def classify(self, tags):
        title = None
        for tag in (tag for tag in tags if tag.name and tag.name == 'title'):
            title = tag.getText()
        return title, 1, 0

    def _get_filename_postfix(self):
        return ''

    def title(self):
        return 'TITLE BASED CLASSIFICATION'

    def description(self):
        return """Classifies jobs according to the job name found in the title tag. The title tag is used without
        changes as the class label."""

    def label(self):
        return 'title-based'
