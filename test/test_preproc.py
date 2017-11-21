import unittest

from bs4 import *
from bs4 import Tag
from hamcrest import *

from src import preproc as testee


def read_sample_file(filename):
    with open('./resources/' + filename + '.html', 'r', encoding='utf-8') as file:
        return file.read()


def write_extracted_tags(extracted_tags, filename):
    with open('./resources/' + filename + '_extracted.html', 'w+', encoding='utf-8') as file:
        for tag in extracted_tags:
            file.write(str(tag) + '\n')


class TestPreprocessing(unittest.TestCase):
    def test_parse(self):
        # arrange
        markup = read_sample_file('sample_vacancy')
        # act
        soup = testee.parse(markup)
        # assert
        assert_that(soup, equal_to(BeautifulSoup(markup, 'lxml')))

    def test_remove_html_clutter_should_remove_clutter(self):
        # arrange
        soup_cluttered = BeautifulSoup(read_sample_file('sample_vacancy'), 'html.parser')
        # act
        extracted_tags = testee.remove_html_clutter(soup_cluttered)
        # assert
        soup_expected = BeautifulSoup(read_sample_file('sample_vacancy_extracted'), 'html.parser')
        expected_tags = [child for child in soup_expected.children if type(child) is Tag]
        assert_that(extracted_tags, equal_to(expected_tags))

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

    @unittest.skip("removing CDATA is performed automatically atm by using a lxml-parser")
    def test_remove_cdata_removes_cdata(self):
        # arrange
        soup = BeautifulSoup('<html><body><p><![CDATA[ Lorem ipsum ]]>This text should be preserved</p></body></html>',
                             'lxml')
        # act
        result = testee.remove_cdata(soup)
        # assert
        assert_that(str(result), is_('<html><body><p>This text should be preserved</p></body></html>'))
