import pickle

from src import preproc
from src.preprocessing.create_nltk_pos_tagger_german import german_pos_tagger_path
from src.preprocessing.preprocessor import Preprocessor
from src.util import util

german_pos_tagger = None
with open(german_pos_tagger_path, 'rb') as f:
    german_pos_tagger = pickle.load(f)


def split_tag_content(html):
    tags = preproc.extract_relevant_tags(html)
    tags_contents = ((tag.name, tag.getText()) for tag in tags)
    return zip(*tags_contents)


def contents_to_sentences(contents, html_tags):
    for content, html_tag in zip(contents, html_tags):
        content_sents = preproc.to_sentences(content)
        for sent in content_sents:
            yield html_tag, sent


def content_sents_to_wordlist(content_sents):
    for tag, sent in content_sents:
        words = preproc.to_words(sent)
        words = preproc.remove_punctuation(words)
        yield tag, list(words)


def add_pos_tag(content_words):
    for tag, words in content_words:
        yield tag, german_pos_tagger.tag(words)


def content_words_to_stems(content_words):
    for tag, words in content_words:
        yield tag, list((preproc.stem(word), pos_tag) for (word, pos_tag) in words)


class StructuralPreprocessorNVT(Preprocessor):
    def __init__(self):
        super(StructuralPreprocessorNVT, self).__init__()

    def preprocess_single(self, row):
        html_tags, contents = split_tag_content(row.html)
        content_sents = contents_to_sentences(contents, html_tags)
        content_words = content_sents_to_wordlist(content_sents)
        content_words_tagged = add_pos_tag(content_words)
        content_words_tagged_stememd = content_words_to_stems(content_words_tagged)
        processed = []
        for (html_tag, tagged_words) in content_words_tagged_stememd:
            for word, pos_tag in tagged_words:
                processed.append((word, pos_tag, html_tag))
        return processed
