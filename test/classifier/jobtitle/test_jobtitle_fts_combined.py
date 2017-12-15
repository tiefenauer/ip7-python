import unittest

from hamcrest import contains, assert_that, empty, is_, only_contains

from src.classifier.jobtitle import jobtitle_fts_combined
from src.preprocessing.preproc import create_tag


class TestCombinedJobtitleFtsClassifier(unittest.TestCase):

    def test_find_positions_with_no_match_returns_empty_list(self):
        # arrange
        tagged_words = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN')]
        # act
        result = jobtitle_fts_combined.find_positions(tagged_words, 'Bäcker')
        result = list(result)
        # assert
        assert_that(result, is_(empty()))

    def test_find_positions_with_one_match_returns_position(self):
        # arrange
        tagged_words = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN')]
        # act
        result = jobtitle_fts_combined.find_positions(tagged_words, 'Geschäftsführer')
        result = list(result)
        # assert
        assert_that(result, only_contains(3))

    def test_find_positions_with_multiple_matches_returns_all_positions(self):
        # arrange
        tagged_words = [('Wir', 'PPER'),
                        ('suchen', 'VVFIN'),
                        ('einen', 'ART'),
                        ('Geschäftsführer', 'NN'),
                        ('oder', 'KON'),
                        ('einen', 'ART'),
                        ('Geschäftsführer', 'NN')
                        ]
        # act
        result = jobtitle_fts_combined.find_positions(tagged_words, 'Geschäftsführer')
        result = list(result)
        # assert
        assert_that(result, only_contains(3, 6))

    def test_find_variant_positions_returns_all_positions(self):
        # arrange
        tagged_words = [('Wir', 'PPER'),
                        ('suchen', 'VVFIN'),
                        ('einen', 'ART'),
                        ('Geschäftsführer', 'NN'),
                        ('oder', 'KON'),
                        ('eine', 'ART'),
                        ('Geschäftsführerin', 'NN'),
                        ('Geschäftsführerin', 'NN')
                        ]
        # act
        result = jobtitle_fts_combined.find_variant_positions(tagged_words, ['Geschäftsführer', 'Geschäftsführerin'])
        result = list(result)
        # assert
        assert_that(result, only_contains(
            ('Geschäftsführer', [3]),
            ('Geschäftsführerin', [6, 7])
        ))

    def test_find_variants_in_tags_returns_variants_with_positions_and_tagged_words(self):
        # arrange
        tagged_words_1 = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN')]
        tagged_words_2 = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('eine', 'ART'), ('Geschäftsführerin', 'NN')]
        tagged_words_3 = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN'),
                          ('oder', 'KON'), ('eine', 'ART'), ('Geschäftsführerin', 'NN')]
        tagged_words_4 = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN'),
                          ('und', 'KON'), ('einen', 'ART'), ('Geschäftsführer', 'NN')]
        pos_tagged_html_tags = [
            ('h1', tagged_words_1),
            ('h2', tagged_words_2),
            ('h3', tagged_words_3),
            ('h4', tagged_words_4),
        ]
        variants = ['Geschäftsführer', 'Geschäftsführerin']
        # act
        result = jobtitle_fts_combined.find_variants_in_tags(pos_tagged_html_tags, variants)
        result = list(result)
        # assert
        assert_that(result, only_contains(
            (0, 'h1', 'Geschäftsführer', [3], tagged_words_1),
            (1, 'h2', 'Geschäftsführerin', [3], tagged_words_2),
            (2, 'h3', 'Geschäftsführer', [3], tagged_words_3),
            (2, 'h3', 'Geschäftsführerin', [6], tagged_words_3),
            (3, 'h4', 'Geschäftsführer', [3, 6], tagged_words_4)
        ))

    def test_find_known_jobs_returns_list_of_matches(self):
        # arrange
        tagged_words_1 = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN')]
        tagged_words_2 = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('eine', 'ART'), ('Geschäftsführerin', 'NN')]
        tagged_words_3 = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN'),
                          ('oder', 'KON'), ('einen', 'ART'), ('Elektrotechniker', 'NN')]
        tagged_words_4 = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN'),
                          ('und', 'KON'), ('einen', 'ART'), ('Elektrotechniker/in', 'ADJA'), ('als', 'APPR'),
                          ('Geschäftsführer', 'NN')]
        tags = [
            create_tag('h1', ' '.join(word for (word, tag) in tagged_words_1)),
            create_tag('h2', ' '.join(word for (word, tag) in tagged_words_2)),
            create_tag('h3', ' '.join(word for (word, tag) in tagged_words_3)),
            create_tag('h4', ' '.join(word for (word, tag) in tagged_words_4))
        ]
        known_jobs = [
            ('Geschäftsführer', ['Geschäftsführer', 'Geschäftsführerin', 'Geschäftsführer/in']),
            ('Elektrotechniker', ['Elektrotechniker', 'Elektro-Techniker', 'Elektrotechniker/in', 'ElektrotechnikerIn'])
        ]
        # act
        result = jobtitle_fts_combined.find_known_jobs(tags, known_jobs)
        result = list(result)
        # assert
        assert_that(result, contains(
            (0, 'h1', 'Geschäftsführer', [3], tagged_words_1),
            (1, 'h2', 'Geschäftsführerin', [3], tagged_words_2),
            (2, 'h3', 'Geschäftsführer', [3], tagged_words_3),
            (3, 'h4', 'Geschäftsführer', [3, 8], tagged_words_4),
            (2, 'h3', 'Elektrotechniker', [6], tagged_words_3),
            (3, 'h4', 'Elektrotechniker/in', [6], tagged_words_4)
        ))

    def test_improve_search_result_no_improvement_possible_returns_matchin_job(self):
        # arrange
        tagged_words = [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN')]
        matching_job = 'Geschäftsführer'
        position = 3
        # act
        result = jobtitle_fts_combined.improve_search_result(tagged_words, matching_job, position)
        # assert
        assert_that(result, is_(matching_job))

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

    def test_to_sentences_one_sentence_returns_map_tag_name_sentences(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Wir suchen einen Geschäftsführer.'),
            create_tag('h2', 'Willst du dich bewerben?'),
            create_tag('p', 'Erfahrung wird überbewertet!')
        ]
        # act
        result = jobtitle_fts_combined.to_sentences_map(html_tags)
        result = list(result)
        # asser
        assert_that(result, only_contains(
            ('h1', 'Wir suchen einen Geschäftsführer.'),
            ('h2', 'Willst du dich bewerben?'),
            ('p', 'Erfahrung wird überbewertet!')
        ))

    def test_to_sentences_multi_sentence_returns_one_entry_per_sentence(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Wir suchen einen Geschäftsführer. Willst du dich bewerben?'),
            create_tag('p', 'Erfahrung wird überbewertet!')
        ]
        # act
        result = jobtitle_fts_combined.to_sentences_map(html_tags)
        result = list(result)
        # asser
        assert_that(result, only_contains(
            ('h1', 'Wir suchen einen Geschäftsführer.'),
            ('h1', 'Willst du dich bewerben?'),
            ('p', 'Erfahrung wird überbewertet!')
        ))

    def test_to_pos_tagged_words_one_sentence_returns_map_of_tag_to_pos_tagged_sentences(self):
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

    def test_to_pos_tagged_words_compound_word(self):
        # arrange
        html_tags = [
            create_tag('h2', 'Polymechaniker / CNC Fräser 80% - 100% (m/w)')
        ]
        # act
        result = jobtitle_fts_combined.to_pos_tagged_words(html_tags)
        result = list(result)
        # assert
        assert_that(result, contains(
            ('h2', [('Polymechaniker', 'NE'), ('/', '$('), ('CNC', 'NE'), ('Fräser', 'NE'), ('80', 'CARD'), ('%', 'NN'),
                    ('-', '$('), ('100', 'CARD'), ('%', 'NN'), ('(', '$('), ('m/w', 'XY'), (')', '$(')])
        ))
