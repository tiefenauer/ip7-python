from src import preproc
from src.preprocessing.preprocessor import Preprocessor


def split_words_by_tag(html):
    tags = preproc.extract_relevant_tags(html)
    for html_tag, content in ((tag.name, tag.getText()) for tag in tags):
        for sent in preproc.to_sentences(content):
            words = preproc.to_words(sent)
            words = preproc.remove_punctuation(words)
            yield html_tag, list(words)


def content_words_to_stems(tagged_word_lists):
    for tagged_word_list in tagged_word_lists:
        yield [(preproc.stem(word), pos_tag) for (word, pos_tag) in tagged_word_list]


class StructuralPreprocessorNVT(Preprocessor):
    def __init__(self):
        super(StructuralPreprocessorNVT, self).__init__()

    def preprocess_single(self, row):
        # html to map tag-> ['word1', 'word2', '...'] (1 entry per sentence)
        words_by_tag = list(split_words_by_tag(row.html)) # evaluate generator because markup might not contain any relevant tags
        if not words_by_tag:
            return []
        html_tags, word_lists = zip(*words_by_tag)
        tagged_words_list = preproc.pos_tag(word_lists)
        tagged_stems_lists = content_words_to_stems(tagged_words_list)

        processed = []
        for tagged_stem_list, html_tag in zip(tagged_stems_lists, html_tags):
            for stem, pos_tag in tagged_stem_list:
                processed.append((stem, pos_tag, html_tag))
        return processed
