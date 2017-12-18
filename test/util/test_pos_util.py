import unittest

from hamcrest import assert_that, contains, is_

from src.preprocessing import preproc
from src.util import pos_util


class TestPOSUtil(unittest.TestCase):

    def test_find_job_name_with_known_job_single_word_returns_known_job(self):
        # arrange
        sentence = 'Wir suchen einen Geschäftsführer'
        # act
        result = pos_util.find_job(sentence)
        # assert
        assert_that(result, is_('Geschäftsführer'))

    def test_find_job_name_with_known_job_multi_word_returns_known_job(self):
        # arrange
        sentence = 'Wir suchen einen Vertriebsleiter Einkauf'
        # act
        result = pos_util.find_job(sentence)
        # assert
        assert_that(result, is_('Vertriebsleiter Einkauf'))

    def test_find_job_name_with_unknown_job_findy_by_mw(self):
        # single word
        assert_that(pos_util.find_job('Wir suchen eine Geschäftsführung (m/w)'), is_('Geschäftsführung'))
        assert_that(pos_util.find_job('Wir suchen eine Geschäftsführung m/w'), is_('Geschäftsführung'))
        assert_that(pos_util.find_job('Wir suchen eine Geschäftsführung (w/m)'), is_('Geschäftsführung'))
        assert_that(pos_util.find_job('Wir suchen eine Geschäftsführung w/m'), is_('Geschäftsführung'))
        # multi word
        assert_that(pos_util.find_job('Wir suchen eine Geschäftsführung Einkauf (m/w)'), is_('Geschäftsführung Einkauf'))
        assert_that(pos_util.find_job('Wir suchen eine Geschäftsführung Einkauf m/w'), is_('Geschäftsführung Einkauf'))
        assert_that(pos_util.find_job('Wir suchen eine Geschäftsführung Einkauf (w/m)'), is_('Geschäftsführung Einkauf'))
        assert_that(pos_util.find_job('Wir suchen eine Geschäftsführung Einkauf w/m'), is_('Geschäftsführung Einkauf'))

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
