import re
import unittest

from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

from src.jobtitle import jobtitle_extractor as testee


class TestJobTitleExtractor(unittest.TestCase):
    def test_count_variant_returns_correct_count(self):
        # arrange
        string = '<p>Schneider Schneiderin Schneider/-in Schneider/in</p>'
        # act
        result = testee.count_variant('Schneider', string)
        # assert
        assert_that(result, is_(1), "When counting a variant only count exact matches of that variant")

    def test_find_all_returns_all_matches_with_count(self):
        # arrange
        tags = [
            '<p>Assistent</p>',
            '<p>Koch Koch</p>',
            '<p>Schneider Schneider Schneider</p>'
        ]
        # act
        result = testee.find_all_matches(tags, ['Koch', 'Schneider', 'Assistent'])
        # assert
        assert_that(result, contains_inanyorder(
            (1, 'Assistent'),
            (2, 'Koch'),
            (3, 'Schneider')
        ))

    def test_find_all_returns_variants_as_one_suffix_er(self):
        # arrange
        tags = ['<p>Schneider Schneiderin Schneider/-in Schneider/in Schneider (m/w)</p>']
        # act
        result = testee.find_all_matches(tags, ['Schneider'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Schneider')))

    def test_find_all_returns_variants_as_one_suffix_eur(self):
        # arrange
        tags = ['<p>Coiffeur Coiffeuse Coiffeur/-euse Coiffeur/euse Coiffeur (m/w)</p>']
        # act
        result = testee.find_all_matches(tags, ['Coiffeur'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Coiffeur')))

    def test_find_all_returns_variants_as_one_suffix_mann(self):
        # arrange
        tags = ['<p>Kaufmann Kauffrau Kaufmann/-frau Kaufmann/frau Kaufmann (m/w)</p>']
        # act
        result = testee.find_all_matches(tags, ['Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Kaufmann')))

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


def result_item_with_name_and_context(job_name, context):
    return IsResultMatchingJob(job_name, context)


class IsResultMatchingJob(BaseMatcher):
    def __init__(self, job_name, job_contexts):
        self.job_name = job_name
        self.job_contexts = job_contexts

    def _matches(self, item):
        if item['job_name'] != self.job_name:
            return False
        if set(item['job_contexts']) != set(self.job_contexts):
            return False
        return True

    def describe_to(self, description):
        description.append_text('result item with item[\'job_name\'] matching \'') \
            .append_text(self.job_name) \
            .append_text('\' and item[\'job_context\'] matching \'') \
            .append_text(self.job_contexts) \
            .append_text('\'')
