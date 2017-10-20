import re

import nltk

from src.train.util import create_contexts

suffix_female = r"(\/-?in)|(\/-?euse)|(\/-?frau)"
suffix_male = r"(\/-?er)|(\/-?eur)|(\/-?mann)"

regex_fm = r"((\/?-?in)|(\/?-?euse)|(\/?-?frau))"
regex_mw = r"\s*\(?m\/w\)?"


def find_matches(str, job_name):
    for match in re.finditer(job_name, str):
        context_token = determine_context_token(str, match)
        yield create_result_item(str, context_token)


def determine_context_token(str, match_obj):
    start = match_obj.start()
    end = match_obj.end()
    str_sub = str[start:]
    exact_match = str[start:end]
    # check if match can be expanded to include \-in, \-euse and \-frau
    match_fm = check_if_exact_match_can_be_expanded_with_regex(exact_match, regex_fm, str_sub)
    if match_fm:
        return match_fm
    # check if match can be expanded to include (m/w)
    match_mw = check_if_exact_match_can_be_expanded_with_regex(exact_match, regex_mw, str_sub)
    if match_mw:
        return match_mw
    return exact_match


def check_if_exact_match_can_be_expanded_with_regex(exact_match, regex, str_sub):
    expanded_match = re.match(exact_match + regex, str_sub)
    if expanded_match and expanded_match.start() == 0:
        return expanded_match.string[:expanded_match.end()]
    return None


def create_result_item(str, context_token):
    return {
        'job_name': context_token,
        'job_contexts': create_contexts(str, context_token)
    }


def remove_gender(str):
    stripped = re.sub(suffix_male, '', str)
    stripped = re.sub(suffix_female, '', str)
    return stripped


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
