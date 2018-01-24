from src.preprocessing import preproc
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor


def split_words_by_tag(tags):
    for html_tag, content in ((tag.name, tag.getText()) for tag in tags):
        for sent in preproc.to_sentences(content):
            words = preproc.to_words(sent)
            words = preproc.remove_punctuation(words)
            yield html_tag, list(words)


def content_words_to_lemmata(tagged_word_lists):
    for tagged_word_list in tagged_word_lists:
        yield [(preproc.lemmatize_word(word, pos).lower(), pos) for (word, pos) in tagged_word_list]


class StructuralPreprocessor(RelevantTagsPreprocessor):

    def preprocess_single(self, row):
        relevant_tags = super(StructuralPreprocessor, self).preprocess_single(row)
        # evaluate generator already here because markup might not contain any relevant tags
        relevant_tags = list(relevant_tags)
        if not relevant_tags:
            return []
        # html to map tag-> ['word1', 'word2', '...'] (1 entry per sentence)
        words_by_tag = split_words_by_tag(relevant_tags)
        html_tags, word_lists = zip(*words_by_tag)
        tagged_words_list = preproc.pos_tag(word_lists)
        tagged_lemmata_lists = content_words_to_lemmata(tagged_words_list)

        processed = []
        for tagged_lemmata_list, html_tag in zip(tagged_lemmata_lists, html_tags):
            for lemma, pos_tag in tagged_lemmata_list:
                processed.append((lemma, pos_tag, html_tag))
        return processed
