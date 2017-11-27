import unittest

from hamcrest import assert_that, contains, contains_inanyorder
from hamcrest.core.base_matcher import BaseMatcher

from src.preprocessing import structural_preprocessor_nvt


class TestStructuralPreprocessorNVT(unittest.TestCase):
    def test_split_tag_content_splits_into_tag_and_content(self):
        # arrange
        markup = """
        <h1>Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.</h1>
        <p>Dies ist noch ein Inhalt.</p>
        """
        # act
        html_tags, contents = structural_preprocessor_nvt.split_tag_content(markup)
        # assert
        assert_that(html_tags, contains('h1', 'p'))
        assert_that(contents, contains(
            'Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.',
            'Dies ist noch ein Inhalt.'
        ))

    def test_contents_to_sentences(self):
        # arrange
        contents = [
            'Dies ist ein Test zum schauen ob es funktioniert. Dies ist ein anderer Satz.',
            'Dies ist noch ein Inhalt.'
        ]
        html_tags = ['h1', 'p']
        # act
        result = structural_preprocessor_nvt.contents_to_sentences(contents, html_tags)
        # assert
        assert_that(result, contains(
            ('h1', 'Dies ist ein Test zum schauen ob es funktioniert.'),
            ('h1', 'Dies ist ein anderer Satz.'),
            ('p', 'Dies ist noch ein Inhalt.')
        ))

    def test_content_sents_to_wordlist_returns_wordlist(self):
        # arrange
        content_sents = [
            ('h1', 'Dies ist ein Test zum schauen ob es funktioniert'),
            ('h1', 'Dies ist ein anderer Satz'),
            ('p', 'Dies ist noch ein Inhalt')
        ]
        # act
        result = structural_preprocessor_nvt.content_sents_to_wordlist(content_sents)
        # assert
        assert_that(result, contains(
            ('h1', ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert']),
            ('h1', ['Dies', 'ist', 'ein', 'anderer', 'Satz']),
            ('p', ['Dies', 'ist', 'noch', 'ein', 'Inhalt'])
        ))

    def test_content_sents_to_wordlist_returns_wordlist_without_punctuation(self):
        # arrange
        content_sents = [
            ('h1', 'Dies ist ein Test zum schauen, ob es funktioniert.'),
            ('h1', 'Dies ist ein anderer Satz.'),
            ('p', 'Dies ist noch ein Inhalt!')
        ]
        # act
        result = structural_preprocessor_nvt.content_sents_to_wordlist(content_sents)
        # assert
        assert_that(result, contains(
            ('h1', ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert']),
            ('h1', ['Dies', 'ist', 'ein', 'anderer', 'Satz']),
            ('p', ['Dies', 'ist', 'noch', 'ein', 'Inhalt'])
        ))

    def test_add_pos_tag_adds_pos_tag_to_list(self):
        # arrange
        content_words = [
            ('h1', ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert']),
            ('h1', ['Dies', 'ist', 'ein', 'anderer', 'Satz']),
            ('p', ['Dies', 'ist', 'noch', 'ein', 'Inhalt'])
        ]
        # act
        result = structural_preprocessor_nvt.add_pos_tag(content_words)
        result = list(result)
        # assert
        assert_that(result, contains(
            result_item('h1', [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('Test', 'NN'), ('zum', 'APPRART'),
                               ('schauen', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')]),
            result_item('h1', [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('Satz', 'NN')]),
            result_item('p', [('Dies', 'PDS'), ('ist', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('Inhalt', 'NN')])
            ))

    def test_content_words_to_stems_converts_words_to_stem(self):
        # arrange
        content_words = [
            ('h1', ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert']),
            ('h1', ['Dies', 'ist', 'ein', 'anderer', 'Satz']),
            ('p', ['Dies', 'ist', 'noch', 'ein', 'Inhalt'])
        ]
        # act
        result = structural_preprocessor_nvt.content_words_to_stems(content_words)
        # assert
        assert_that(result, contains(
            ('h1', ['dies', 'ist', 'ein', 'test', 'zum', 'schau', 'ob', 'es', 'funktioniert']),
            ('h1', ['dies', 'ist', 'ein', 'anderer', 'satz']),
            ('p', ['dies', 'ist', 'noch', 'ein', 'inhalt'])
        ))


def result_item(html_tag, pos_tagged_words):
    return IsTupleMatching(html_tag, pos_tagged_words)


class IsTupleMatching(BaseMatcher):
    def __init__(self, html_tag, pos_tagged_words):
        self.html_tag = html_tag
        self.pos_tagged_words = pos_tagged_words

    def _matches(self, item):
        return self.html_tag == item[0] \
               and self.pos_tagged_words == item[1]

    def describe_to(self, description):
        description.append_text('tuple matching html_tag=\'') \
            .append_text(self.html_tag) \
            .append_text(' and pos_tagged_words=') \
            .append_text(self.pos_tagged_words)
