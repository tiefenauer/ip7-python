import collections

from src.dataimport.known_jobs import KnownJobs
from src.preprocessing import preproc
from src.util import loe_util, jobtitle_util

mw_tokens = ['m/w', 'w/m', 'm/f', 'f/m',
             'M/W', 'W/M', 'M/F', 'F/M']


def find_jobs(sentence):
    jobs = []
    # find known jobs
    for hit in find_job_by_keyword(sentence, KnownJobs()):
        jobs.append((hit, 'known-job'))
    # find by m/w patterns
    sentence_without_percentage = loe_util.remove_percentage(sentence)
    for hit in find_job_by_keyword(sentence_without_percentage, mw_tokens):
        jobs.append((hit, 'mw'))
    # find by percentages
    sentence_without_mw = jobtitle_util.remove_mw(sentence)
    for hit in find_job_by_keyword(sentence_without_mw, loe_util.find_all_loe(sentence_without_mw)):
        jobs.append((hit, 'loe'))
    # find by gender forms
    # sentence_without_mw_and_percentage = loe_util.remove_percentage(sentence_without_mw)
    # jobs += find_job_by_keyword(sentence_without_mw_and_percentage, ['/in', '/-in'])

    # search by keyword: gender
    # for match in jobtitle_util.find_all_genderized(sentence):
    #     gender_job = expand_left_right(sentence.split(match[0])[0], sentence)
    # if gender_job:
    #     yield gender_job
    return jobs


def find_job_by_keyword(sentence, keywords):
    # job_names = []
    for keyword in keywords:
        if keyword in sentence:
            job_name = expand_left_right(keyword, sentence)
            if job_name:
                yield job_name
            # job_names.append(job_name)

    # return job_names


def expand_left_right(token, sentence):
    if token not in sentence:
        return None
    job_name_tokens = preproc.to_words(token)
    sentence_tokens = [word for word in preproc.to_words(sentence) if word not in ['(', ')']]

    ix_from, ix_to = calculate_positions(job_name_tokens, sentence_tokens)

    sentence_pos = preproc.pos_tag(sentence_tokens)
    left = sentence_pos[:ix_from]
    right = sentence_pos[ix_to:]

    initial_content = [token] if token not in mw_tokens and not loe_util.is_percentate(token) else []
    tokens = collections.deque(initial_content)
    search_left(left, tokens)
    search_right(right, tokens)
    return ' '.join(tokens)


def search_left(pos_tagged_words, tokens=collections.deque()):
    i = len(pos_tagged_words) - 1
    while 0 <= i:
        word, pos_tag = pos_tagged_words[i]
        if is_part_of_name(word, pos_tag):
            tokens.appendleft(word)
        else:
            break
        i -= 1
    return tokens


def search_right(pos_tagged_words, tokens=collections.deque()):
    i = 0
    while 0 <= i < len(pos_tagged_words):
        word, pos_tag = pos_tagged_words[i]
        if is_part_of_name(word, pos_tag):
            tokens.append(word)
        else:
            break
        i += 1
    return tokens


def is_part_of_name(word, pos_tag):
    return is_noun(pos_tag) or word in ['/']


def is_noun(pos_tag):
    return pos_tag[0] in ['N', 'F']


def is_punctuation(pos_tag):
    return pos_tag.startswith('$')


def calculate_positions(job_name_tokens, sentence_tokens):
    ix_from = [i for i, word in enumerate(sentence_tokens) if job_name_tokens[0] in word][0]
    ix_to = ix_from + len(job_name_tokens)
    return ix_from, ix_to
