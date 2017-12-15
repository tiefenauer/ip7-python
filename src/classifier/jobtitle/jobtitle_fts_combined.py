from src.classifier.jobtitle.jobtitle_classifier import JobtitleClassifier
# from src.classifier.jobtitle.jobtitle_fts_classifier_htmltag_based import job_name_variants
from src.classifier.tag_classifier import TagClassifier
from src.preprocessing import preproc


def find_positions(tagged_words, search_word):
    """return matching job_name and position within sentence"""
    return (i for (i, (word, tag)) in enumerate(tagged_words) if word == search_word)


def find_variant_positions(tagged_words, job_variants):
    """return positions of all job variants in tagged_words"""
    for variant in job_variants:
        positions = list(find_positions(tagged_words, variant))
        if positions:
            yield variant, positions


def find_variants_in_tags(pos_tagged_html_tags, job_variants):
    """search for occurrences of job variants in pos_tagged_html_tags
    Result is returned as 3-tuple: (html_tag, job_variant, [position1, position2, ...])
    """
    for html_tag, pos_tagged_words in pos_tagged_html_tags:
        variant_positions = find_variant_positions(pos_tagged_words, job_variants)
        for variant, positions in variant_positions:
            yield html_tag, variant, positions, pos_tagged_words


def find_known_jobs(html_tags, known_job_variants):
    pos_tagged_html_tags = to_pos_tagged_words(html_tags)
    # evaluate generator already here because it is iterated over once for each job name
    pos_tagged_html_tags = list(pos_tagged_html_tags)
    for job_name, job_variants in known_job_variants:
        search_results_for_job = find_variants_in_tags(pos_tagged_html_tags, job_variants)
        for html_tag, variant, positions, tagged_words in search_results_for_job:
            yield html_tag, variant, positions, tagged_words


def improve_search_result(tagged_words, matching_job, position):
    """improve search result by evaluating adjacent POS tags"""
    improved_job_name = matching_job
    # evaluate to the left
    return improved_job_name


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
