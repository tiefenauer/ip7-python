import unittest

from hamcrest import contains, assert_that

from src.classifier.jobtitle import jobtitle_fts_combined
from src.preprocessing.preproc import create_tag


class TestCombinedJobtitleFtsClassifier(unittest.TestCase):

    def test_to_word_list_returns_map_tag_word_list(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Foo bar'),
            create_tag('p', 'baz baq')
        ]
        # act
        result = jobtitle_fts_combined.to_word_list(html_tags)
        # assert
        assert_that(result, contains(
            ('h1', ['Foo', 'bar']),
            ('p', ['baz', 'baq'])
        ))

    def test_to_pos_tagged_words_returns_map_tag_word_pos_tag(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Wir suchen einen Geschäftsführer'),
            create_tag('p', 'Erfahrung wird überbewertet')
        ]
        # act
        result = jobtitle_fts_combined.to_pos_tagged_words(html_tags)
        # assert
        assert_that(result, contains(
            ('h1', [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN')]),
            ('p', [('Erfahrung', 'NN'), ('wird', 'VAFIN'), ('überbewertet', 'VVPP')])
        ))

    def test_find_known_jobs_returns_result(self):
        # arrange
        words_per_tag = [
            ('h1', [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN')]),
            ('p', [('Haus', 'NN'), ('ist', 'VAFIN'), ('gebaut', 'VVPP')]),
            ('p', [('Schreiner', 'NN'), ('sind', 'VAFIN'), ('überbewertet', 'VVPP')])
        ]
        # act
        result = jobtitle_fts_combined.find_known_jobs(words_per_tag)
        # assert
        assert_that(result, contains(
            ('h1', [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN')], [('Geschäftsführer', 3)]),
            ('p', [('Schreiner', 'NN'), ('und', 'KONJ'), ('Bäcker', 'NN'), ('sind', 'VAFIN'), ('überbewertet', 'VVPP')])
        ))