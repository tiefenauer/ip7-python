import re

from src.dataimport.known_jobs import KnownJobs
# job title patterns
from src.preprocessing import preproc

pattern_hyphenated = re.compile(r'(?=\S*[-])([a-zA-Z-]+)')
# dynamic patterns
pattern_suffix = "{}((in)|(euse)|(frau))"
pattern_slashed = "{}((\/?-?in)|(\/?-?euse)|(\/?-?frau))"

# job title suffix patterns: general
suffix_pattern_eur_euse = re.compile(r'(eur)?\/?-?([Ee]use)$')
suffix_pattern_mann_frau = re.compile(r'(mann)?\/?-?([Ff]rau)$')
suffix_pattern_in = re.compile(r'\/?-?(\(?[iI]n\)?)$')
suffix_pattern_mw = re.compile(r'\s?(\(?m\/?w\)?)')
suffix_pattern_wm = re.compile(r'\s?(\(?w\/?m\)?)')
suffix_pattern_person = re.compile(r'(person)$')

# job title suffix patterns: male forms
suffix_pattern_eur = re.compile(r'(eur)$')
suffix_pattern_mann = re.compile(r'(mann)$')
suffix_pattern_er = re.compile(r'(er)$')


def find(string, job_name):
    jn_m = to_male_form(job_name)
    jn_m = re.escape(jn_m)
    jn_f = to_female_form(job_name)
    jn_f = re.escape(jn_f)

    pattern = pattern_suffix.format(jn_m)  # match suffix form: Schneiderin, Coiffeuse, Kauffrau
    pattern += '|' + pattern_slashed.format(jn_m)  # match slashed form: Schneider/-in, Coiffeur/-euse, Kaufmann/-frau
    pattern += '|' + jn_f  # match female form: Schneiderin, Coiffeuse, Kauffrau
    pattern += '|' + jn_m  # match male form: Schneider, Coiffeur, Kaufmann
    return re.finditer(pattern, string)


def to_male_form(job_name):
    jn = re.sub(suffix_pattern_eur_euse, 'eur', job_name)
    jn = re.sub(suffix_pattern_mann_frau, 'mann', jn)
    jn = re.sub(suffix_pattern_person, 'mann', jn)
    jn = re.sub(suffix_pattern_in, '', jn)
    jn = re.sub(suffix_pattern_mw, '', jn)
    jn = re.sub(suffix_pattern_wm, '', jn)
    return jn


def to_female_form(job_name):
    jn = re.sub(suffix_pattern_eur, 'euse', job_name)
    jn = re.sub(suffix_pattern_mann, 'frau', jn)
    jn = re.sub(suffix_pattern_er, 'erin', jn)
    jn = re.sub(suffix_pattern_person, 'frau', jn)
    return jn


def to_female_form_camel_cased(job_name):
    jn = re.sub(suffix_pattern_er, 'erIn', job_name)
    return jn


def to_female_form_brackets(job_name):
    jn = re.sub(suffix_pattern_er, 'er(in)', job_name)
    return jn


def to_slashed_form(job_name):
    jn = re.sub(suffix_pattern_eur, 'eur/euse', job_name)
    jn = re.sub(suffix_pattern_mann, 'mann/frau', jn)
    jn = re.sub(suffix_pattern_er, 'er/in', jn)
    return jn


def to_slashed_hyphen_form(job_name):
    jn = re.sub(suffix_pattern_eur, 'eur/-euse', job_name)
    jn = re.sub(suffix_pattern_mann, 'mann/-frau', jn)
    jn = re.sub(suffix_pattern_er, 'er/-in', jn)
    return jn


def to_mw_form_brackets_slashed(job_name):
    return to_male_form(job_name) + ' (m/w)'


def to_mw_form_slashed(job_name):
    return to_male_form(job_name) + ' m/w'


def to_mw_form(job_name):
    return to_male_form(job_name) + ' mw'


def to_wm_form_brackets_slashed(job_name):
    return to_male_form(job_name) + ' (w/m)'


def to_wm_form_slashed(job_name):
    return to_male_form(job_name) + ' w/m'


def to_wm_form(job_name):
    return to_male_form(job_name) + ' wm'


def to_spaced_form(job_name_1, job_name_2):
    return job_name_1.title() + ' ' + job_name_2.title()


def to_concatenated_form(job_name_1, job_name_2):
    return job_name_1.title() + job_name_2.lower()


def to_hyphenated_form(job_name_1, job_name_2):
    return job_name_1.title() + '-' + job_name_2.title()


def is_hyphenated(job_name):
    return pattern_hyphenated.match(job_name)


def create_gender_variants(job_name):
    return {to_male_form(job_name),
            to_female_form(job_name),
            to_female_form_camel_cased(job_name),
            to_female_form_brackets(job_name),
            to_slashed_form(job_name),
            to_slashed_hyphen_form(job_name),
            to_mw_form(job_name),
            to_mw_form_slashed(job_name),
            to_mw_form_brackets_slashed(job_name),
            to_wm_form(job_name),
            to_wm_form_slashed(job_name),
            to_wm_form_brackets_slashed(job_name),
            }


def create_write_variants(job_name):
    write_variants = set()
    write_variants.add(job_name)
    if is_hyphenated(job_name):
        job_name_parts = re.findall('([a-zA-Z]+)', job_name)
        part1 = job_name_parts[0]
        part2 = job_name_parts[1]
        job_concatenated = to_concatenated_form(part1, part2.lower())
        job_spaced = to_spaced_form(part1, part2)
        write_variants.add(job_concatenated)
        write_variants.add(job_spaced)
    else:
        for known_job in KnownJobs():
            if known_job.lower() in job_name:
                part1 = job_name.split(known_job.lower())[0].strip()
                job_concatenated = to_concatenated_form(part1, known_job.lower())
                job_spaced = to_spaced_form(part1, known_job)
                job_hyphenated = to_hyphenated_form(part1, known_job)
                write_variants.add(job_concatenated)
                write_variants.add(job_spaced)
                write_variants.add(job_hyphenated)

    return write_variants


def create_variants(job_name):
    variants = set()
    write_variants = create_write_variants(job_name)
    variants.update(write_variants)
    for write_variant in write_variants:
        gender_variants = create_gender_variants(write_variant)
        variants.update(gender_variants)

    return variants


def count_variant(variant, string):
    """Count EXACT occurrences of variant with respect to word boundaries. This means an occurrence will only be counted
    if it is a full word (not including hyphenated or slashed forms.

    Example

    variant          string                                     count
    ---------------------------------------------------------------------------
    Polymechaniker   Polymechaniker                             1
    Polymechaniker   Polymechanikerin                           0
    Polymechaniker   PolymechanikerIn                           0
    Polymechaniker   Polymechaniker/Polymechanikerin            1

    Anatomy of regex:
    (?<!\w){}       left word boundary and the variant ({} will be replaced by the variant)
    (?! ...)        negative lookahead for one of the following variants
        [\w]            word character
        \s*\(?m/?w\)?   space(s) and the (m/w) suffix in any form
        (\/-)           slash followed by a hyphen
        (\/[IEa-z])     slash followed by uppercase I or E and a lowercase character
                            -> this prevents e.g. Polymechaniker being counted in Polymechanikerin while still counting
                               Polymechaniker in Polymechaniker/Polymechanikerin
                               or analogous Coiffeur is not counted in Coiffeur/euse but in Coiffeur/Coiffeuse
    """
    # pattern = r'(?<!\w){}(?![\w/]|\s\(m/w\)|\/)'.format(re.escape(variant))  # old pattern
    pattern = r'(?<!\w){}(?![\w]|\s*\(?m/?w\)?|(\/-)|(\/[IEa-z]))'.format(re.escape(variant))
    matches = re.findall(pattern, string)
    return len(matches)


def normalize_job_name(job_name):
    if not job_name:
        return job_name
    return preproc.stem(to_male_form(job_name)).lower()


def normalize_text(text):
    if not text:
        return text
    no_special_chars = preproc.remove_special_chars(text)
    words = preproc.to_words(no_special_chars)
    no_stopwords = (preproc.remove_stop_words(words))
    no_gender = (to_male_form(word) for word in no_stopwords)
    return (word for word in preproc.stem(no_gender))
