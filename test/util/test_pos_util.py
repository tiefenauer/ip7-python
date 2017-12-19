import unittest
from unittest import skip

from hamcrest import assert_that, contains, is_, only_contains, empty

from src.preprocessing import preproc
from src.util import pos_util


class TestPOSUtil(unittest.TestCase):

    def test_find_jobs_with_no_matches_returns_None(self):
        # arrange
        sentence = """An über 60 Standorten in der gesamten Schweiz machen über 400 Lernende ihre Ausbildung in den 
        verschiedensten Berufsrichtungen"""
        # act
        result = pos_util.find_jobs(sentence)
        # asser
        assert_that(list(result), is_(empty()))

    def test_find_jobs_with_known_job_single_word_returns_known_job(self):
        # arrange
        sentence = 'Wir suchen einen Geschäftsführer'
        # act
        result = pos_util.find_jobs(sentence)
        # assert
        assert_that(result, only_contains(('Geschäftsführer', 'known-job')))

    def test_find_jobs_with_known_job_multi_word_returns_known_job(self):
        # arrange
        sentence = 'Wir suchen einen Vertriebsleiter Einkauf'
        # act
        result = pos_util.find_jobs(sentence)
        # assert
        assert_that(result, only_contains(('Vertriebsleiter Einkauf', 'known-job')))

    @skip('not supported yet')
    def test_find_jobs_with_unknown_job_findy_by_gender_form(self):
        result = pos_util.find_jobs('Leiter/in Familienausgleichskassen')
        result = list(result)
        assert_that(result, only_contains(('Leiter Familienausgleichskassen', 'gender')))

    def test_find_jobs_with_unknown_job_findy_by_mw(self):
        # single word
        assert_that(pos_util.find_jobs('Wir suchen eine Geschäftsführung (m/w)'),
                    only_contains(('Geschäftsführung', 'mw')))
        assert_that(pos_util.find_jobs('Wir suchen eine Geschäftsführung m/w'),
                    only_contains(('Geschäftsführung', 'mw')))
        assert_that(pos_util.find_jobs('Wir suchen eine Geschäftsführung (w/m)'),
                    only_contains(('Geschäftsführung', 'mw')))
        assert_that(pos_util.find_jobs('Wir suchen eine Geschäftsführung w/m'),
                    only_contains(('Geschäftsführung', 'mw')))
        # multi word
        assert_that(pos_util.find_jobs('Wir suchen Geschäftsführung Einkauf (m/w)'),
                    only_contains(('Geschäftsführung Einkauf', 'mw')))
        assert_that(pos_util.find_jobs('Wir suchen Geschäftsführung Einkauf m/w'),
                    only_contains(('Geschäftsführung Einkauf', 'mw')))
        assert_that(pos_util.find_jobs('Wir suchen Geschäftsführung Einkauf (w/m)'),
                    only_contains(('Geschäftsführung Einkauf', 'mw')))
        assert_that(pos_util.find_jobs('Wir suchen Geschäftsführung Einkauf w/m'),
                    only_contains(('Geschäftsführung Einkauf', 'mw')))

    def test_find_jobs_with_unknown_job_find_by_by_loe(self):
        # single word
        assert_that(pos_util.find_jobs('Wir suchen eine Geschäftsführung 100%'),
                    only_contains(('Geschäftsführung', 'loe')))
        assert_that(pos_util.find_jobs('Wir suchen eine Geschäftsführung 80%'),
                    only_contains(('Geschäftsführung', 'loe')))
        assert_that(pos_util.find_jobs('Wir suchen eine Geschäftsführung 80-100%'),
                    only_contains(('Geschäftsführung', 'loe')))
        assert_that(pos_util.find_jobs('Wir suchen eine Geschäftsführung 80%-100%'),
                    only_contains(('Geschäftsführung', 'loe')))
        # multi word
        assert_that(pos_util.find_jobs('Wir suchen Geschäftsführung Einkauf 100%'),
                    only_contains(('Geschäftsführung Einkauf', 'loe')))
        assert_that(pos_util.find_jobs('Wir suchen Geschäftsführung Einkauf 80%'),
                    only_contains(('Geschäftsführung Einkauf', 'loe')))
        assert_that(pos_util.find_jobs('Wir suchen Geschäftsführung Einkauf 80-100%'),
                    only_contains(('Geschäftsführung Einkauf', 'loe')))
        assert_that(pos_util.find_jobs('Wir suchen Geschäftsführung Einkauf 80%-100%'),
                    only_contains(('Geschäftsführung Einkauf', 'loe')))

    def test_find_jobs_with_unknown_job_find_by_mw_and_percentage(self):
        # arrange
        sentence_1 = 'Wir suchen eine Geschäftsführung (m/w) 100%'
        sentence_2 = 'Wir suchen eine Geschäftsführung 100% (m/w)'
        # act/assert
        result_1 = pos_util.find_jobs(sentence_1)
        result_2 = pos_util.find_jobs(sentence_2)
        result_1 = list(result_1)
        result_2 = list(result_2)
        assert_that(result_1, only_contains(('Geschäftsführung', 'mw'), ('Geschäftsführung', 'loe')))
        assert_that(result_2, only_contains(('Geschäftsführung', 'mw'), ('Geschäftsführung', 'loe')))

    def test_find_jobs_with_unknown_job_find_by_gender_form(self):
        pass

    def test_search_left_returns_all_nouns(self):
        # arrange
        sentence = 'Wir suchen einen motivierten Stellvertreter Geschäftsführer'
        pos_tokens = preproc.pos_tag(preproc.to_words(sentence))
        # act
        result = pos_util.search_left(pos_tokens)
        assert_that(result, contains('Stellvertreter', 'Geschäftsführer'))

    def test_search_right_returns_all_nouns(self):
        # arrange
        sentence = 'Head EFZ für verschieedene Aufgaben'
        pos_tokens = preproc.pos_tag(preproc.to_words(sentence))
        # act
        result = pos_util.search_right(pos_tokens)
        assert_that(result, contains('Head', 'EFZ'))

    def test_expand_left_right_without_match_returns_None(self):
        # arrange
        job_name = 'Bäcker'
        sentence = 'Wir suchen einen Geschäftsführer'
        # act
        result = pos_util.expand_left_right(job_name, sentence)
        assert_that(result, is_(None))

    def test_expand_left_right_with_simple_name_returns_exact_match(self):
        # arrange
        job_name = 'Polymechaniker'
        sentence = 'Wir suchen einen Polymechaniker'
        # act
        result = pos_util.expand_left_right(job_name, sentence)
        assert_that(result, is_('Polymechaniker'))

    def test_expand_left_right_with_compound_name_returns_compound_name(self):
        # arrange
        job_name = 'Compliance Officer'
        sentence = 'Wir suchen einen Compliance Officer mit Erfahrung'
        # act
        result = pos_util.expand_left_right(job_name, sentence)
        assert_that(result, is_('Compliance Officer'))

    def test_expand_left_right_with_expandable_job_name_returns_expandable_job_name(self):
        # arrange
        job_name_1 = 'Polymechaniker'
        job_name_2 = 'CNC Fräser'
        sentence = 'Polymechaniker / CNC Fräser 80% - 100% (m/w)'
        # act
        result_1 = pos_util.expand_left_right(job_name_1, sentence)
        result_2 = pos_util.expand_left_right(job_name_2, sentence)
        # assert
        assert_that(result_1, is_('Polymechaniker / CNC Fräser'))
        assert_that(result_2, is_('Polymechaniker / CNC Fräser'))

    def test_expand_left_right_with_expandable_compound_job_name_returns_expandable_job_name(self):
        # arrange
        job_name = 'Compliance Officer'
        sentence = 'Team Head Compliance Officer Premium Clients Switzerland (80-100%)'
        # act
        result = pos_util.expand_left_right(job_name, sentence)
        assert_that(result, is_('Team Head Compliance Officer Premium Clients Switzerland'))

    def test_calculate_positions_with_exact_match(self):
        # arrange
        job_name_tokenized = preproc.to_words('Erzieher')
        sentence_tokenized = preproc.to_words('Erzieher / Gruppenleitung')
        # act
        result = pos_util.calculate_positions(job_name_tokenized, sentence_tokenized)
        assert_that(result, is_((0, 1)))

    def test_calculate_positions_with_fuzzy_match(self):
        # arrange
        job_name_tokenized = preproc.to_words('Erzieher')
        sentence_tokenized = preproc.to_words('Erzieherin / Gruppenleitung')
        # act
        result = pos_util.calculate_positions(job_name_tokenized, sentence_tokenized)
        assert_that(result, is_((0, 1)))
