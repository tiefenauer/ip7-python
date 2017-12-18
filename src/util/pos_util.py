import collections

from src.preprocessing import preproc


def expand_left_right(job_name, sentence):
    if job_name not in sentence:
        return None
    job_name_tokens = preproc.to_words(job_name)
    sentence_tokens = preproc.to_words(sentence)

    ix_from, ix_to = calculate_positions(job_name_tokens, sentence_tokens)

    sentence_pos = preproc.pos_tag(sentence_tokens)
    left = sentence_pos[:ix_from]
    right = sentence_pos[ix_to:]

    tokens = collections.deque([job_name])
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
