import re

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
    jn = re.sub('\/?-?([iI]n)$', '', jn)
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


def create_variants(job_name):
    return {to_male_form(job_name),
            to_female_form(job_name),
            to_female_form_camel_cased(job_name),
            to_slashed_form(job_name),
            to_slashed_hyphen_form(job_name),
            to_mw_form(job_name),
            to_mw_form_slashed(job_name),
            to_mw_form_brackets_slashed(job_name),
            to_wm_form(job_name),
            to_wm_form_slashed(job_name),
            to_wm_form_brackets_slashed(job_name),
            }


def count_variant(variant, string):
    pattern = r'(?<!\w){}(?![\w/]|\s\(m/w\))'.format(re.escape(variant))
    matches = re.findall(pattern, string)
    return len(matches)
