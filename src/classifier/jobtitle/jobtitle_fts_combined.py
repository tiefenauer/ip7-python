from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.tag_classifier import TagClassifier
from src.preprocessing import preproc
from src.preprocessing.preproc import german_pos_tagger

german_pos_tagger


def pos_tag_tags(tags):
    for tag in tags:
        words = preproc.to_words(tag.getText())
        tagged_words = german_pos_tagger.tag(words)
        yield tag.name, tagged_words


class CombinedJobtitleClassifier(TagClassifier, JobtitleClassifier):
    """Combines different approaches to one single classifier:
    - FTS approach:
        - known jobs or parts of known jobs are searched in the relevant tags
        - hits in tags with higher priority are preferred over hits in tags with lower priority
    - Structural approach:
        - hits near the top of the page are preferred over hits near the bottom of the page (those may be required skills)
        - hits with patterns suggesting a job title are preferred over hits without such patterns. Suggesting patterns
        need to occur within the same sentence. Suggesting patterns are:
            - wir suchen
            - (m/w)
            - xxx% (level of employment)
            - "in" (place of work)
        - hits in tags with only one sentence are preferred over hits in tags with several sentences
        - hit is expanded with POS-tagged words nearby
        - hit is expanded with
    """

    def classify(self, tags):
        tagged_tags = pos_tag_tags(tags)
        for tag_name, tagged_words in tagged_tags:
            print(tag_name, tagged_words)
        return None

    def title(self):
        return 'Jobtitle Classifier: FTS (advanced)'

    def label(self):
        return 'jobtitle-fts-advanced'

    def get_filename_postfix(self):
        return ''
