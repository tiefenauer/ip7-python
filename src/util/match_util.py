import re

regex_fm = r"(in)|(euse)|(frau)"
regex_fm_slashed = r"((\/?-?in)|(\/?-?euse)|(\/?-?frau))"
regex_mw = r"\s*\(?m\/w\)?"


def determine_context_token(str, match):
    start = match.start()
    end = match.end()
    str_sub = str[start:]
    exact_match = str[start:end]
    # check if match can be expanded to include in, euse and frau
    match_fm = expand_match(exact_match, regex_fm, str_sub)
    if (match_fm):
        return match_fm
    # check if match can be expanded to include /-in, /-euse and /-frau
    match_fm_slashed = expand_match(exact_match, regex_fm_slashed, str_sub)
    if match_fm_slashed:
        return match_fm_slashed
    # check if match can be expanded to include (m/w)
    match_mw = expand_match(exact_match, regex_mw, str_sub)
    if match_mw:
        return match_mw
    return exact_match


def expand_match(exact_match, regex, string):
    expanded_match = re.match(exact_match + regex, string)
    if expanded_match and expanded_match.start() == 0:
        return expanded_match.string[:expanded_match.end()]
    return None


def find_job_name_with_highest_occurrence(matches):
    return next(
        iter(
            sorted(list(matches), key=lambda m: len(m['job_contexts']), reverse=True)
        )
    )['job_name']
