import re
import unittest

from hamcrest import *

from src.util import match_util as testee


class TestMatchUtil(unittest.TestCase):
    def test_determine_context_token_simple_returns_token(self):
        # act
        str = 'create_result_item_with_contexts Schreiner create_result_item_with_contexts'
        match_obj = re.search('Schreiner', str)
        # arrange
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_('Schreiner'))

    def test_determine_context_token_fm_slash_in_returns_token_slash_in(self):
        # arrange
        str = 'create_result_item_with_contexts Schreiner/-in create_result_item_with_contexts'
        match_obj = re.search('Schreiner', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Schreiner/-in"))

    def test_determine_context_token_fm_slash_euse_returns_token_slash_euse(self):
        # arrange
        str = 'create_result_item_with_contexts Coiffeur/-euse create_result_item_with_contexts'
        match_obj = re.search('Coiffeur', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Coiffeur/-euse"))

    def test_determine_context_token_fm_slash_frau_returns_token_slash_frau(self):
        # arrange
        str = 'create_result_item_with_contexts Kaufmann/-frau create_result_item_with_contexts'
        match_obj = re.search('Kaufmann', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Kaufmann/-frau"))

    def test_determine_context_token_fm_in_returns_token_slash_in(self):
        # arrange
        str = 'create_result_item_with_contexts Schreinerin create_result_item_with_contexts'
        match_obj = re.search('Schreiner', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Schreinerin"))

    def test_determine_context_token_fm_euse_returns_token_slash_euse(self):
        # arrange
        str = 'create_result_item_with_contexts Coiffeuse create_result_item_with_contexts'
        match_obj = re.search('Coiff(eur|euse)', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Coiffeuse"))

    def test_determine_context_token_fm_frau_returns_token_slash_frau(self):
        # arrange
        str = 'create_result_item_with_contexts Kauffrau create_result_item_with_contexts'
        match_obj = re.search('Kauf(mann|frau)', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Kauffrau"))

    def test_determine_context_token_mw_returns_token_including_mw(self):
        # arrange
        str = 'create_result_item_with_contexts Sachbearbeiter (m/w) create_result_item_with_contexts'
        match_obj = re.search('Sachbearbeiter', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_('Sachbearbeiter (m/w)'))

    def test_find_job_name_with_highest_occurrence_returns_highest_occurrence(self):
        # arrange
        matches = [
            {'job_name': 'CEO', 'job_contexts': ['context 1', 'context 2', 'context 3']},
            {'job_name': 'Schreiner', 'job_contexts': ['context 1', 'context 2', 'context 3', 'context 4']},
            {'job_name': 'Sekretärin', 'job_contexts': ['context 1', 'context 2']},
        ]
        # act
        result = testee.find_job_name_with_highest_occurrence(matches)
        # assert
        assert_that(result, is_('Schreiner'))
