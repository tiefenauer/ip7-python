import unittest

from hamcrest import assert_that, contains

from src.preprocessing import structural_preprocessor_nvt


class TestStructuralPreprocessorNVT(unittest.TestCase):
    def test_to_html_word_list_returns_list_of_tuples(self):
        # arrange
        html = '<h1>Dies ist ein Test</h1><p>zum schauen ob es funktioniert</p>'
        # act
        result = structural_preprocessor_nvt.to_html_word_list(html)
        # assert
        assert_that(result, contains(
            ('Dies', 'h1'),
            ('ist', 'h1'),
            ('ein', 'h1'),
            ('Test', 'h1'),
            ('zum', 'p'),
            ('schauen', 'p'),
            ('ob', 'p'),
            ('es', 'p'),
            ('funktioniert', 'p')
        ))
