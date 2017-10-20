import re

import nltk

from src.train.util import create_contexts

suffix_female = r"(\/-?in)|(\/-?euse)|(\/-?frau)"
suffix_male = r"(\/-?er)|(\/-?eur)|(\/-?mann)"

regex_gender = r"((\/?-?in)|(\/?-?euse)|(\/?-?frau))"


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
    in_match = re.match(exact_match + regex_gender, str_sub)
    if in_match and in_match.start() == 0:
        return in_match.string[:in_match.end()]
    # check if match can be expanded to include (m/w)
    return exact_match


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
