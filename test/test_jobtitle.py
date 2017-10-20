import re
import unittest

from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

from src.extractor import jobtitle as testee


class TestJobTitleExtractor(unittest.TestCase):
    def test_find_matches_returns_single_match_with_context(self):
        # arrange
        str = 'Wir suchen einen 20-jährigen Schreiner mit 30 Jahren Erfahrung'
        # act
        result = list(testee.find_matches(str, 'Schreiner'))
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Schreiner', {'...-jährigen Schreiner mit 30 Ja...'})
        ))

    def test_find_matches_returns_multiple_matches_with_context(self):
        # arrange
        str = "Wir suchen einen Schreiner und gleich nochmals einen Schreiner, der bei uns arbeitet"
        # act
        result = list(testee.find_matches(str, 'Schreiner'))
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Schreiner', {
                '...hen einen Schreiner und gleic...',
                '...als einen Schreiner, der bei ...'
            })
        ))

    @unittest.skip("need to create context token first")
    def test_find_matches_search_male_finds_female_forms_in(self):
        # arrange
        str = "Wir suchen eine Schreinerin welche gerne arbeitet"
        # act
        result = list(testee.find_matches(str, 'Schreiner'))
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Schreinerin', {'...chen eine Schreinerin welche ge...'})
        ))

    @unittest.skip("need to create context token first")
    def test_find_matches_search_male_finds_female_forms_euse(self):
        # arrange
        str = "Wir suchen eine Coiffeuse welche gerne arbeitet"
        # act
        result = list(testee.find_matches(str, 'Coiffeur'))
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Coiffeuse', {'...chen eine Coiffeuse welche ge...'})
        ))

    @unittest.skip("need to create context token first")
    def test_find_matches_search_male_finds_female_forms_frau(self):
        # arrange
        str = "Wir suchen eine Kauffrau welche gerne arbeitet"
        # act
        result = list(testee.find_matches(str, 'Kaufmann'))
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Kauffrau', {'...chen eine Kauffrau welche ge...'})
        ))

    @unittest.skip("need to create context token first")
    def test_find_matches_search_male_match_contains_male_slash_female(self):
        # Suche nach Kaufmann, Coiffeur, Schreiner: Result Item enthält Kaufmann/-frau, Coiffeur/-euse, Schreiner/-in
        pass

    def test_find_matches_search_male_match_contains_male_slash_female(self):
        # Suche nach Kauffrau, Coiffeuse, Schreinerin: Result Item enthält Kaufmann/-frau, Coiffeur/-euse, Schreiner/-in
        pass

    def test_find_matches_search_female_finds_male_forms(self):
        pass

    def test_find_matches_finds_plurals(self):
        pass

    def test_find_matches_finds_hypenated(self):
        pass

    def test_find_matches_includes_brackets_mw(self):
        pass

    def test_determine_context_token_simple_form_returns_token(self):
        # act
        str = 'bla Schreiner bla'
        match_obj = re.search('Schreiner', str)
        # arrange
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_('Schreiner'))

    def test_determine_context_token_gender_in_returns_token_including_in(self):
        # arrange
        str = 'bla Schreiner/-in bla'
        match_obj = re.search('Schreiner', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Schreiner/-in"))

    def test_determine_context_token_gender_euse_returns_token_including_euse(self):
        # arrange
        str = 'bla Coiffeur/-euse bla'
        match_obj = re.search('Coiffeur', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Coiffeur/-euse"))

    def test_determine_context_token_gender_frau_returns_token_including_frau(self):
        # arrange
        str = 'bla Kaufmann/-frau bla'
        match_obj = re.search('Kaufmann', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Kaufmann/-frau"))

    def test_determine_context_token_mw_returns_token_including_mw(self):
        # arrange
        str = 'bla Sachbearbeiter (m/w) bla'
        match_obj = re.search('Sachbearbeiter', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_('Sachbearbeiter (m/w)'))


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
            .append_text('\'')
