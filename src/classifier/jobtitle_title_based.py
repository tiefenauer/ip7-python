from src.classifier.classification_strategy import ClassificationStrategy


class TitleBasedJobTitleClassifier(ClassificationStrategy):
    TITLE = """TITLE BASED CLASSIFICATION"""
    DESCRIPTION = """Classifies jobs according to the job name found in the title tag. The title tag is used without
    changes as the class label."""

    def classify(self, tags):
        title = None
        for tag in (tag for tag in tags if tag.name and tag.name == 'title'):
            title = tag.getText()
        return title, 1, 0

    def title(self):
        return self.TITLE

    def description(self):
        return self.DESCRIPTION
