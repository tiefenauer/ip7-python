import unittest

from hamcrest import contains, assert_that, empty, is_, only_contains

from src.classifier.jobtitle import jobtitle_fts_combined
from src.classifier.jobtitle.jobtitle_fts_combined import CombinedJobtitleClassifier
from src.preprocessing.preproc import create_tag
from test import testutils

args = testutils.create_dummy_args()
testee = CombinedJobtitleClassifier(args)


class TestCombinedJobtitleFtsClassifier(unittest.TestCase):

    def test_classify_with_improvable_hit(self):
        # arrange
        html_tags = [
            create_tag('h2', 'Polymechaniker / CNC Fräser 80% - 100% (m/w)')
        ]
        # act
        result = testee.classify(html_tags)
        # assert
        assert_that(result, is_('Polymechaniker / CNC Fräser'))

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

    def test_improve_search_result_more_on_right_possible_returns_matchin_job(self):
        # arrange
        tagged_words = [('Polymechaniker', 'NE'), ('/', '$('), ('CNC', 'NE'), ('Fräser', 'NE'), ('80', 'CARD'),
                        ('%', 'NN'), ('-', '$('), ('100', 'CARD'), ('%', 'NN'), ('(', '$('), ('m/w', 'XY'), (')', '$(')]
        # act
        result = jobtitle_fts_combined.improve_search_result(tagged_words, 'Polymechaniker', 0)
        # assert
        assert_that(result, is_('Polymechaniker / CNC Fräser'))

    def test_improve_search_result_more_on_left_and_right(self):
        # arrange
        tagged_words = [('Team', 'NN'), ('Head', 'NE'), ('Compliance', 'FM'), ('Officer', 'FM'), ('Premium', 'FM'),
                        ('Clients', 'FM'), ('Switzerland', 'FM'), ('(', '$('), ('80-100', 'CARD'), ('%', '$('),
                        (')', '$(')]
        # act
        result = jobtitle_fts_combined.improve_search_result(tagged_words, 'Compliance Officer', 2)
        # assert
        assert_that(result, is_('Team Head Compliance Officer Premium Clients Switzerland'))

    def test_to_sentences_map_one_sentence_returns_map_tag_name_sentences(self):
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

    def test_to_sentences_map_multi_sentence_returns_one_entry_per_sentence(self):
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

    def test_to_wordlist_map_returns_tokenized_sentence_including_punctuation(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Wir suchen einen Geschäftsführer. Willst du dich bewerben?'),
            create_tag('p', 'Erfahrung wird überbewertet!')
        ]
        # act
        result = jobtitle_fts_combined.to_wordlist_map(html_tags)
        result = list(result)
        # asser
        assert_that(result, only_contains(
            ('h1', ['Wir', 'suchen', 'einen', 'Geschäftsführer', '.']),
            ('h1', ['Willst', 'du', 'dich', 'bewerben', '?']),
            ('p', ['Erfahrung', 'wird', 'überbewertet', '!'])
        ))

    def test_to_pos_tagged_words_map_returns_map_of_tag_to_pos_tagged_sentences_excluding_punctuation(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Wir suchen einen Geschäftsführer. Willst du dich bewerben?'),
            create_tag('p', 'Erfahrung wird überbewertet!')
        ]
        # act
        result = jobtitle_fts_combined.to_pos_tagged_words_map(html_tags)
        result = list(result)
        # assert
        assert_that(result, contains(
            ('h1', [('Wir', 'PPER'), ('suchen', 'VVFIN'), ('einen', 'ART'), ('Geschäftsführer', 'NN'), ('.', '$.')]),
            ('h1', [('Willst', 'PWS'), ('du', 'PPER'), ('dich', 'PRF'), ('bewerben', 'VVINF'), ('?', '$.')]),
            ('p', [('Erfahrung', 'NN'), ('wird', 'VAFIN'), ('überbewertet', 'VVPP'), ('!', '$.')])
        ))

    def test_to_pos_tagged_words_compound_word(self):
        # arrange
        html_tags = [
            create_tag('h2', 'Polymechaniker / CNC Fräser 80% - 100% (m/w)')
        ]
        # act
        result = jobtitle_fts_combined.to_pos_tagged_words_map(html_tags)
        result = list(result)
        # assert
        assert_that(result, contains(
            ('h2', [('Polymechaniker', 'NE'), ('/', '$('), ('CNC', 'NE'), ('Fräser', 'NE'), ('80', 'CARD'), ('%', 'NN'),
                    ('-', '$('), ('100', 'CARD'), ('%', 'NN'), ('(', '$('), ('m/w', 'XY'), (')', '$(')])
        ))
