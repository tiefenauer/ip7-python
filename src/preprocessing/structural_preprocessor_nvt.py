import pickle

from src import preproc
from src.preprocessing.create_nltk_pos_tagger_german import german_pos_tagger_path
from src.preprocessing.preprocessor import Preprocessor

german_pos_tagger = None
with open(german_pos_tagger_path, 'rb') as f:
    german_pos_tagger = pickle.load(f)


def split_words_by_tag(html):
    tags = preproc.extract_relevant_tags(html)
    for html_tag, content in ((tag.name, tag.getText()) for tag in tags):
        for sent in preproc.to_sentences(content):
            words = preproc.to_words(sent)
            words = preproc.remove_punctuation(words)
            yield html_tag, list(words)


def add_pos_tag(word_list):
    return (german_pos_tagger.tag(words) for words in word_list)


def content_words_to_stems(tagged_word_lists):
    for tagged_word_list in tagged_word_lists:
        yield [(preproc.stem(word), pos_tag) for (word, pos_tag) in tagged_word_list]


class StructuralPreprocessorNVT(Preprocessor):
    def __init__(self):
        super(StructuralPreprocessorNVT, self).__init__()

    def preprocess_single(self, row):
        # html to map tag-> ['word1', 'word2', '...'] (1 entry per sentence)
        tag_wordlist = split_words_by_tag(row.html)
        html_tags, word_lists = zip(*tag_wordlist)
        tagged_word_lists = add_pos_tag(word_lists)
        tagged_stem_lists = content_words_to_stems(tagged_word_lists)
        processed = []
        for tagged_stem_list, html_tag in zip(tagged_stem_lists, html_tags):
            for stem, pos_tag in tagged_stem_list:
                processed.append((stem, pos_tag, html_tag))
        return processed
