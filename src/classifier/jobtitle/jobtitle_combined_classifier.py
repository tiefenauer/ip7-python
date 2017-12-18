from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.jobtitle.jobtitle_features_combined import JobtitleFeaturesCombined
from src.classifier.tag_classifier import TagClassifier
from src.dataimport.known_jobs import KnownJobs
from src.util import pos_util


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

    def predict_class(self, htmltag_sentences_map):
        # find occurrences of known jobs (including variants) in HTML tags together with positional and POS information
        features_list = []
        i_tag_sentence = list(enumerate(htmltag_sentences_map))
        for job_name in KnownJobs():
            for tag_index, (tag_name, sentence) in i_tag_sentence:
                hit = pos_util.expand_left_right(job_name, sentence)
                if hit:
                    features = JobtitleFeaturesCombined(tag_index, hit, tag_name)
                    features_list.append(features)

        if len(features_list) > 0:
            best_match = sorted(features_list)[0]
            return best_match.job_name

        return None

    def title(self):
        return 'Jobtitle Classifier: FTS (advanced)'

    def label(self):
        return 'jobtitle-combined'

    def get_filename_postfix(self):
        return ''
