from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.jobtitle.jobtitle_fts_classifier_htmltag_based import job_name_variants
from src.classifier.tag_classifier import TagClassifier
from src.preprocessing import preproc


def find_known_jobs(words_per_tag, known_jobs=job_name_variants):
    pass


def to_pos_tagged_words(html_tags):
    words_per_tag = to_word_list(html_tags)
    for tag_name, words in words_per_tag:
        yield tag_name, preproc.pos_tag(words)


def to_word_list(html_tags):
    return ((tag.name, preproc.to_words(tag.getText())) for tag in html_tags)


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

    def classify(self, html_tags):
        words_per_tag = to_pos_tagged_words(html_tags)
        for tag_name, tagged_words in words_per_tag:
            print(tag_name, tagged_words)
        return None

    def title(self):
        return 'Jobtitle Classifier: FTS (advanced)'

    def label(self):
        return 'jobtitle-fts-advanced'

    def get_filename_postfix(self):
        return ''
