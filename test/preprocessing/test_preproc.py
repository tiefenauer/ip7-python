import unittest

from bs4 import *
from hamcrest import *

from src.preprocessing import preproc as testee
from test.testutils import read_sample_file


class TestPreprocessing(unittest.TestCase):
    def test_parse(self):
        # arrange
        markup = read_sample_file('sample_vacancy')
        # act
        soup = testee.parse(markup)
        # assert
        assert_that(soup, is_(BeautifulSoup(markup, 'lxml')))

    def test_create_tag_creates_tag(self):
        # arrange/act
        tag_p_foo = testee.create_tag('p', 'foo')
        tag_p_empty = testee.create_tag('p', '')
        tag_p_none = testee.create_tag('p', None)
        tag_foo = testee.create_tag('foo', 'bar')
        # assert
        assert_that(tag_p_foo.name, is_('p'))
        assert_that(tag_p_foo.getText(), is_('foo'))
        assert_that(tag_p_empty.name, is_('p'))
        assert_that(tag_p_empty.getText(), is_(''))
        assert_that(tag_p_none.name, is_('p'))
        assert_that(tag_p_none.getText(), is_(''))
        assert_that(tag_foo.name, is_('foo'))

    def test_create_tags_creates_list_of_tags(self):
        # arrange / act
        result = testee.create_tags([
            ('h1', 'foo'),
            ('p', 'bar'),
            ('foo', 'bar')
        ])
        # assert
        assert_that(len(result), is_(3))
        assert_that(result[0].name, is_('h1'))
        assert_that(result[0].getText(), is_('foo'))
        assert_that(result[1].name, is_('p'))
        assert_that(result[1].getText(), is_('bar'))
        assert_that(result[2].name, is_('foo'))
        assert_that(result[2].getText(), is_('bar'))

    def test_create_tag_from_markup_creates_tag(self):
        # arrange
        markup = '<p>foo</p>'
        markup_empty = '<p></p>'
        markup_invalid = '<foo>bar</foo>'
        markup_nomarkup = 'foo bar'
        # act/assert
        assert_that(testee.create_tag_from_markup(markup).name, is_('p'))
        assert_that(testee.create_tag_from_markup(markup).getText(), is_('foo'))
        assert_that(testee.create_tag_from_markup(markup_empty).name, is_('p'))
        assert_that(testee.create_tag_from_markup(markup_empty).getText(), is_(''))
        assert_that(testee.create_tag_from_markup(markup_invalid).name, is_('foo'))
        assert_that(testee.create_tag_from_markup(markup_invalid).getText(), is_('bar'))
        assert_that(testee.create_tag_from_markup(markup_nomarkup), is_('foo bar'))

    def test_get_children_with_flat_tag_returns_empty_list(self):
        # arrange
        tag = testee.create_tag_from_markup('<p></p>')
        # act
        children = testee.get_children(tag)
        # assert
        assert_that(children, is_(empty()))

    def test_get_children_with_nested_tag_returns_empty_list(self):
        # arrange
        tag = testee.create_tag_from_markup('<div><p></p></div>')
        # act
        children = testee.get_children(tag)
        # assert
        assert_that(len(children), is_(1))
        assert_that(children[0].name, is_('p'))

    def test_contains_only_strings_with_flat_tag_returns_True(self):
        # arrange
        tag = testee.create_tag_from_markup('<p>Some Content</p>')
        children = list(tag.children)
        # act
        result = testee.contains_only_strings(children)
        # assert
        assert_that(result, is_(True))

    def test_contains_only_strings_with_flat_tag_returns_False(self):
        # arrange
        tag = testee.create_tag_from_markup('<div>Some Content <p>Some nestedContent</p></div>')
        children = list(tag.children)
        # act
        result = testee.contains_only_strings(children)
        # assert
        assert_that(result, is_(False))

    def test_contains_only_semantic_markup_with_only_semantic_markup_returns_True(self):
        # arrange
        tag_strong = testee.create_tag_from_markup('<p>some <strong>important</strong> content <br/> and a break</p>')
        tag_b = testee.create_tag_from_markup('<p>some <b>important</b> content </p> and a <br/> break')
        tag_strong_b = testee.create_tag_from_markup(
            '<p>some <strong>very</strong> very <b>important</b> content and a <br/> break</p>')
        # act/assert
        assert_that(testee.contains_only_semantic_markup(tag_strong), is_(True))
        assert_that(testee.contains_only_semantic_markup(tag_b), is_(True))
        assert_that(testee.contains_only_semantic_markup(tag_strong_b), is_(True))

    def test_contains_only_strong_or_b_children_with_only_strong_or_b_returns_False(self):
        # arrange
        tag_strong = testee.create_tag_from_markup(
            '<p>some <strong>important</strong> content <p>some other content</p></p>')
        tag_b = testee.create_tag_from_markup('<p>some <b>important</b> content <p>some other content</p></p>')
        tag_strong_b = testee.create_tag_from_markup(
            '<p>some <strong>very</strong> very <b>important</b> content <p>some other content</p></p>')
        # act/assert
        assert_that(testee.contains_only_semantic_markup(tag_strong), is_(False))
        assert_that(testee.contains_only_semantic_markup(tag_b), is_(False))
        assert_that(testee.contains_only_semantic_markup(tag_strong_b), is_(False))

    def test_tag_is_atomic_with_atomic_tag_returns_True(self):
        # arrange
        tag_p_empty = testee.create_tag_from_markup('<p></p>')
        tag_p = testee.create_tag_from_markup('<p>Some content</p>')
        tag_strong = testee.create_tag_from_markup('<p>Some <strong>important</strong> content</p>')
        tag_b = testee.create_tag_from_markup('<p>Some <b>important</b> content</p>')
        tag_strong_b = testee.create_tag_from_markup('<p>Some <strong>very</strong> <b>important</b> content</p>')
        # act/assert
        assert_that(testee.tag_is_atomic(tag_p_empty), is_(True))
        assert_that(testee.tag_is_atomic(tag_p), is_(True))
        assert_that(testee.tag_is_atomic(tag_strong), is_(True))
        assert_that(testee.tag_is_atomic(tag_b), is_(True))
        assert_that(testee.tag_is_atomic(tag_strong_b), is_(True))

    def test_tag_is_atomic_with_atomic_tag_returns_False(self):
        # arrange
        tag_p = testee.create_tag_from_markup('<p>Some <p>nested content</p></p>')
        tag_strong = testee.create_tag_from_markup('<p>Some <strong>important</strong> <p>nested content</p></p>')
        tag_b = testee.create_tag_from_markup('<p>Some <b>important</b> <p>nested content</p></p>')
        tag_strong_b = testee.create_tag_from_markup(
            '<p>Some <strong>very</strong> <b>important</b> <p>nested content</p></p>')
        # act/assert
        assert_that(testee.tag_is_atomic(tag_p), is_(False))
        assert_that(testee.tag_is_atomic(tag_strong), is_(False))
        assert_that(testee.tag_is_atomic(tag_b), is_(False))
        assert_that(testee.tag_is_atomic(tag_strong_b), is_(False))

    def test_remove_strong_and_b_tags_removes_tags(self):
        # arrange
        tag_strong = testee.create_tag_from_markup('<p>This is some <strong>important</strong> content</p>')
        tag_b = testee.create_tag_from_markup('<p>This is some <b>important</b> content</p>')
        # act
        tag_strong_removed = testee.remove_strong_and_b_tags(tag_strong)
        tag_b_removed = testee.remove_strong_and_b_tags(tag_b)
        # assert
        assert_that(str(tag_strong_removed), is_('<p>This is some important content</p>'))
        assert_that(str(tag_b_removed), is_('<p>This is some important content</p>'))

    def test_to_words_splits_into_nltk_words(self):
        # arrange
        text = 'Lehrstelle als Logistiker/in (Distribution) EFZ'
        # act
        result = testee.to_words(text)
        # assert
        assert_that(result, contains('Lehrstelle', 'als', 'Logistiker/in', '(', 'Distribution', ')', 'EFZ'))

    def test_to_sentences_splits_into_nltk_sentences(self):
        # arrange
        text = 'Dies ist ein Satz. Ist dies eine Frage? Dies ist ein Ausruf!'
        # act
        result = testee.to_sentences(text)
        # assert
        assert_that(result, contains(
            'Dies ist ein Satz.',
            'Ist dies eine Frage?',
            'Dies ist ein Ausruf!'
        ))

    def test_remove_special_chars_does_not_remove_forward_slash_or_hyphen(self):
        assert_that(testee.remove_special_chars('Logistiker/in'), is_('Logistiker/in'))
        assert_that(testee.remove_special_chars('Logistiker/-in'), is_('Logistiker/-in'))

    def test_remove_special_chars_removes_numeric_chars(self):
        # arrange
        text = 'Auftragsleiter/-in (w/m) 80% Heizung für die Nordwestschweiz'
        # act
        result = testee.remove_special_chars(text)
        # assert
        assert_that(result, is_('Auftragsleiter/-in w/m Heizung für die Nordwestschweiz'))

    def test_remove_special_chars_from_string_removes_special_chars(self):
        # arrange
        text = 'Lehrstelle als Logistiker/in (Distribution) EFZ'
        # act
        result = testee.remove_special_chars(text)
        # assert
        assert_that(result, is_('Lehrstelle als Logistiker/in Distribution EFZ'))

    def test_remove_special_chars_from_iterable_removes_special_chars(self):
        # arrange
        text = ['Lehrstelle', 'als', 'Logistiker/in', '(Distribution)', 'EFZ']
        # act
        result = testee.remove_special_chars(text)
        # assert
        assert_that(result, contains('Lehrstelle', 'als', 'Logistiker/in', 'Distribution', 'EFZ'))

    def test_remove_special_chars_from_string_with_only_special_chars(self):
        # arrange
        text = 'foo (!) bar'
        # act
        result = testee.remove_special_chars(text)
        # assert
        assert_that(result, is_('foo bar'))

    def test_remove_stopwords_from_string_should_remove_stopwords(self):
        # arrange/act
        result = testee.remove_stop_words("Man ist nur dann ein Superheld, wenn man sich selbst für super hält!")
        # assert
        assert_that(result, is_('Man Superheld, super hält!'))

    def test_remove_stopwords_from_iterable_result_should_not_contain_stopwords(self):
        # arrange/act
        result = testee.remove_stop_words(
            ['Man', 'ist', 'nur', 'dann', 'ein', 'Superheld', 'wenn', 'man', 'sich', 'selbst', 'für', 'super', 'hält'])
        # assert
        assert_that(list(result), is_(['Man', 'Superheld', 'super', 'hält']))

    def test_stem_single_word_returns_stem(self):
        # arrange/act
        aufeinand = testee.stem('aufeinander')
        kategori = testee.stem('kategorie')
        # assert
        assert_that(aufeinand, is_('aufeinand'))
        assert_that(kategori, is_('kategori'))

    def test_stem_multiple_words_returns_stems(self):
        # arrange
        sentence = testee.stem('aufeinander kategorie')
        words = testee.stem(['aufeinander', 'kategorie'])
        # act
        sentence_stemmed = testee.stem(sentence)
        words_stemmed = testee.stem(words)
        # assert
        assert_that(sentence_stemmed, is_('aufeinand kategori'))
        assert_that(list(words_stemmed), is_(['aufeinand', 'kategori']))

    def test_pos_tag_with_single_list_adds_pos_tag_to_words(self):
        # arrange
        word_list = ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert']
        # act
        result = testee.pos_tag(word_list)
        # assert
        assert_that(result, is_(
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('Test', 'NN'), ('zum', 'APPRART'),
             ('schauen', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')]
        ))

    def test_pos_tag_with_multiple_list_adds_pos_tag_to_words(self):
        # arrange
        word_lists = [
            ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert'],
            ['Dies', 'ist', 'ein', 'anderer', 'Satz'],
            ['Dies', 'ist', 'noch', 'ein', 'Inhalt']
        ]
        # act
        result = testee.pos_tag(word_lists)
        # assert
        assert_that(result, contains(
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('Test', 'NN'), ('zum', 'APPRART'),
             ('schauen', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')],
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('Satz', 'NN')],
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('Inhalt', 'NN')]
        ))

    def test_text_list_to_sentence_list_returns_one_sentence_list_per_text(self):
        # arrange
        text_list = [
            'Dies ist Satz eins. Dies ist Satz zwei.',
            'Dies ist Satz drei. Dies ist Satz vier.',
        ]
        # act
        result = testee.text_list_to_sentence_list(text_list)
        # assert
        assert_that(result, contains(
            'Dies ist Satz eins.',
            'Dies ist Satz zwei.',
            'Dies ist Satz drei.',
            'Dies ist Satz vier.'
        ))

    def test_sentence_list_to_word_list_returns_one_wordlist_per_sentence(self):
        # arrange
        sentence_list = [
            'Dies ist ein einfacher Satz.',
            'Und das gleich nochmals einer.'
        ]
        # act
        result = testee.sentence_list_to_word_list(sentence_list)
        # assert
        assert_that(result, contains(
            ['Dies', 'ist', 'ein', 'einfacher', 'Satz', '.'],
            ['Und', 'das', 'gleich', 'nochmals', 'einer', '.']
        ))

    def test_is_iterable_and_not_string(self):
        assert_that(testee.is_iterable_and_not_string('foo bar'), is_(False))
        assert_that(testee.is_iterable_and_not_string(['foo', 'bar']), is_(True))

    def test_is_nested_list(self):
        # arrange
        nested_list = [[1, 2, 3], ['foo', 'bar']]
        simple_list = [1, 2, 3]
        # act/assert
        assert_that(testee.is_nested_list(nested_list), is_(True))
        assert_that(testee.is_nested_list(simple_list), is_(False))

    def test_is_nested_list_with_generator_does_not_evaluate_generator(self):
        # arrange
        generator = (i for i in [1, 2, 3])
        # act
        result = testee.is_nested_list(generator)
        # assert
        assert_that(result, is_(False))
        assert_that(len(list(generator)), is_(3))

    def test_is_generator(self):
        assert_that(testee.is_generator((i for i in [1, 2, 3])), is_(True))
        assert_that(testee.is_generator([1, 2, 3]), is_(False))
