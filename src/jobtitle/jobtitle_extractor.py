import re

import nltk

from src.jobtitle import jobtitle_matcher
from src.util.util import create_contexts

regex_fm = r"(in)|(euse)|(frau)"
regex_fm_slashed = r"((\/?-?in)|(\/?-?euse)|(\/?-?frau))"
regex_mw = r"\s*\(?m\/w\)?"


def extract_job_titles(tag_str, job_names):
    for job_name in job_names:
        variants = jobtitle_matcher.create_search_group(job_name)
        if any(job_name_variant in tag_str for job_name_variant in variants):
            count = 0
            for variant in variants:
                count += count_variant(variant, tag_str)
            yield (job_name, count)


def find_all_matches(tags, job_names):
    html_text = "".join(str(tag) for tag in tags)
    for job_name in job_names:
        variants = jobtitle_matcher.create_search_group(job_name)
        if any(job_name_variant in html_text for job_name_variant in variants):
            count = 0
            for variant in variants:
                count += count_variant(variant, html_text)
            yield (count, job_name)


def count_variant(variant, string):
    # \b...\b(?![\/]) --> match on word boundary but do not consider '/' as a word boundary
    pattern = re.compile(r'\b%s\b(?![\/])' % variant)
    matches = re.findall(pattern, string)
    return len(matches)


def create_result_item(str, context_token):
    return {
        'job_name': context_token,
        'job_contexts': create_contexts(str, context_token)
    }


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
