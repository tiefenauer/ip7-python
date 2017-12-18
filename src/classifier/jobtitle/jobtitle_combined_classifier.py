import collections

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.jobtitle.jobtitle_features_combined import JobtitleFeaturesCombined
from src.classifier.tag_classifier import TagClassifier
from src.dataimport.known_jobs import KnownJobs
from src.preprocessing import preproc


def calculate_positions(job_name_tokens, sentence_tokens):
    ix_from = [i for i, word in enumerate(sentence_tokens) if job_name_tokens[0] in word][0]
    ix_to = ix_from + len(job_name_tokens)
    return ix_from, ix_to


def find_job(job_name, sentence):
    if job_name not in sentence:
        return None
    job_name_tokens = preproc.to_words(job_name)
    sentence_tokens = preproc.to_words(sentence)

    ix_from, ix_to = calculate_positions(job_name_tokens, sentence_tokens)

    sentence_pos = preproc.pos_tag(sentence_tokens)
    left = sentence_pos[:ix_from]
    right = sentence_pos[ix_to:]

    tokens = collections.deque([job_name])
    i = len(left) - 1
    while 0 <= i:
        word, pos_tag = left[i]
        if pos_tag[0] in ['N', 'F'] or pos_tag[0] == '$' and word in ['/']:
            tokens.appendleft(word)
        else:
            break
        i -= 1
    i = 0
    while 0 <= i < len(right):
        word, pos_tag = right[i]
        if pos_tag[0] in ['N', 'F'] or pos_tag[0] == '$' and word in ['/']:
            tokens.append(word)
        else:
            break
        i += 1
    return ' '.join(tokens)


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
                hit = find_job(job_name, sentence)
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
