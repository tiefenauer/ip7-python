import re

from src.dataimport.known_jobs_tsv_importer import KnownJobsImporter

pattern_hyphenated = re.compile('(?=\S*[-])([a-zA-Z-]+)')
pattern_suffix = r"{}((in)|(euse)|(frau))"
pattern_slashed = r"{}((\/?-?in)|(\/?-?euse)|(\/?-?frau))"


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
    jn = re.sub('(eur)?\/?-?(euse)$', 'eur', job_name)
    jn = re.sub('(mann)?\/?-?(frau)$', 'mann', jn)
    jn = re.sub('\/?-?(\(?[iI]n\)?)$', '', jn)
    jn = re.sub('\s?(\(?m\/?w\)?)', '', jn)
    jn = re.sub('\s?(\(?w\/?m\)?)', '', jn)
    return jn


def to_female_form(job_name):
    jn = re.sub('(eur)$', 'euse', job_name)
    jn = re.sub('(mann)$', 'frau', jn)
    jn = re.sub('(er)$', 'erin', jn)
    return jn


def to_female_form_camel_cased(job_name):
    jn = re.sub('(er)$', 'erIn', job_name)
    return jn


def to_female_form_brackets(job_name):
    jn = re.sub('(er)$', 'er(in)', job_name)
    return jn


def to_slashed_form(job_name):
    jn = re.sub('(eur)$', 'eur/euse', job_name)
    jn = re.sub('(mann)$', 'mann/frau', jn)
    jn = re.sub('(er)$', 'er/in', jn)
    return jn


def to_slashed_hyphen_form(job_name):
    jn = re.sub('(eur)$', 'eur/-euse', job_name)
    jn = re.sub('(mann)$', 'mann/-frau', jn)
    jn = re.sub('(er)$', 'er/-in', jn)
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
        for known_job in KnownJobsImporter():
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
    pattern = r'(?<!\w){}(?![\w/]|\s\(m/w\))'.format(re.escape(variant))
    matches = re.findall(pattern, string)
    return len(matches)
