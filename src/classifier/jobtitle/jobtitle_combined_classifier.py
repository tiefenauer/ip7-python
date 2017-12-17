import collections

from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
from src.classifier.jobtitle.jobtitle_features_combined import JobtitleFeaturesCombined
from src.classifier.tag_classifier import TagClassifier
from src.dataimport.known_job_variants import KnownJobVariants
from src.preprocessing import preproc


def find_job(job_name, sentence):
    if job_name not in sentence:
        return None
    job_name_tokens = preproc.to_words(job_name)
    sentence_tokens = preproc.to_words(sentence)

    jn_ix_from = sentence_tokens.index(job_name_tokens[0])
    jn_ix_to = jn_ix_from + len(job_name_tokens)

    sentence_pos = preproc.pos_tag(sentence_tokens)
    left = sentence_pos[:jn_ix_from]
    right = sentence_pos[jn_ix_to:]

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


def to_sentences_map(html_tags):
    for tag in html_tags:
        for sent in preproc.to_sentences(tag.getText()):
            yield tag.name, sent


known_job_variants = KnownJobVariants()


def search_jobs(html_tags, job_variants=known_job_variants):
    for job_name, job_variants in job_variants:
        for variant in job_variants:
            sentences_with_variant = ((tag, sent) for (tag, sent) in to_sentences_map(html_tags) if variant in sent)
            for tag_index, (html_tag, sentence) in enumerate(sentences_with_variant):
                hit = find_job(variant, sentence)
                if hit:
                    yield tag_index, html_tag, hit


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
        # find occurrences of known jobs (including variants) in HTML tags together with positional and POS information
        features_list = [JobtitleFeaturesCombined(tag_index, hit, html_tag)
                         for tag_index, html_tag, hit in search_jobs(html_tags)]

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
