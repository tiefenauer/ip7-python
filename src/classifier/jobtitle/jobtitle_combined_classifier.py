from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.tag_classifier import TagClassifier


class CombinedJobtitleClassifier(TagClassifier, JobtitleClassifier):
    def classify(self, tags):
        pass

    def title(self):
        return 'Jobtitle Classifier: Combined (FTS + semantic + POS-Tags + HTML-Tags)'

    def label(self):
        return 'jobtitle-combined'

    def get_filename_postfix(self):
        return ''
