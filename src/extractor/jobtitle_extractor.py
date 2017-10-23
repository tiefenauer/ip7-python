import re

import nltk

from src.train.util import create_contexts

regex_fm = r"(in)|(euse)|(frau)"
regex_fm_slashed = r"((\/?-?in)|(\/?-?euse)|(\/?-?frau))"
regex_mw = r"\s*\(?m\/w\)?"


def find_all_matches(string, job_names):
    for job_name in job_names:
        jn_m = to_male_form(job_name)
        jn_f = to_female_form(job_name)
        regex_jn_m_or_w = r"({})|({})".format(re.escape(jn_m), re.escape(jn_f))
        for match in re.finditer(regex_jn_m_or_w, string):
            context_token = determine_context_token(string, match)
            yield create_result_item(string, context_token)


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


def to_male_form(job_name):
    jn = re.sub('(euse)$', 'eur', job_name)
    jn = re.sub('(frau)$', 'mann', jn)
    jn = re.sub('(in)$', '', jn)
    return jn


def to_female_form(job_name):
    jn = re.sub('(eur)$', 'euse', job_name)
    jn = re.sub('(mann)$', 'frau', jn)
    jn = re.sub('(er)$', 'erin', jn)
    return jn


def expand_match(exact_match, regex, string):
    expanded_match = re.match(exact_match + regex, string)
    if expanded_match and expanded_match.start() == 0:
        return expanded_match.string[:expanded_match.end()]
    return None


def create_result_item(str, context_token):
    return {
        'job_name': context_token,
        'job_contexts': create_contexts(str, context_token)
    }


def find_job_name_with_highest_occurrence(matches):
    return next(
        iter(
            sorted(list(matches), key=lambda m: len(m['job_contexts']), reverse=True)
        )
    )['job_name']


def tokenize_dom(dom_elements):
    tokens = []
    for el in dom_elements:
        sentences = nltk.sent_tokenize(el.text, 'german')
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        pos_tokens = [nltk.pos_tag(tokens=sent, lang='german') for sent in sentences]
        for tagged_sent in pos_tokens:
            for (word, pos) in tagged_sent:
                tokens.append((word, pos, el.name))
    return tokens


def npchunk_features(sentence, i, history):
    word, pos = sentence[i]
    if i == 0:
        prevword, prevpos = '<START>', '<START>'
    else:
        prevword, prevpos = sentence[i - 1]
    return {
        'pos': pos,
        'word': word,
        'prevword': prevword,
        'prevpos': prevpos
    }


def job_title_features(tag):
    features = {}
    features['html-tag-0'] = ''
    features['html-tag-1'] = ''
    features['html-tag-2'] = ''
    return features


class ConsecutiveNPChunkTagger(nltk.TaggerI):
    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history)
                train_set.append((featureset, tag))
                history.append(tag)
        self.classifier = nltk.MaxentClassifier.train(train_sents, algorithm='megam', trace=0)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)


class ConsecutiveNPChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        tagged_sents = [[((word, tag), chunk) for (word, tag, chunk) in nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(word, tag, chunk) for ((word, tag), chunk) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)
