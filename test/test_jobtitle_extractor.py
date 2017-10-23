import re
import unittest

from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

from src.extractor import jobtitle_extractor as testee


class TestJobTitleExtractor(unittest.TestCase):
    def test_find_matches_should_only_return_matched_job_names(self):
        # arrange
        dom = 'Lorem Arzt ipsum dolor sit amet, Bauer consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.'
        # act
        result = testee.find_matches(dom, ['Arzt', 'Lehrer', 'Bauer'])
        # assert
        assert_that(len(list(result)), is_(2))

    def test_find_matches_returns_single_match_with_context(self):
        # arrange
        str = 'Wir suchen einen 20-jährigen Schreiner mit 30 Jahren Erfahrung'
        # act
        result = testee.find_matches(str, ['Schreiner'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Schreiner', {'...-jährigen Schreiner mit 30 Ja...'})
        ))

    def test_find_matches_returns_multiple_matches_with_context(self):
        # arrange
        string = "Wir suchen einen Schreiner und gleich nochmals einen Schreiner, der bei uns arbeitet"
        # act
        result = testee.find_matches(string, ['Schreiner'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Schreiner', {
                '...hen einen Schreiner und gleic...',
                '...als einen Schreiner, der bei ...'
            })
        ))

    def test_find_matches_search_male_finds_female_forms_in(self):
        # arrange
        string = "Wir suchen eine Schreinerin welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Schreiner'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Schreinerin', {'...chen eine Schreinerin welche ge...'})
        ))

    def test_find_matches_search_male_finds_female_forms_euse(self):
        # arrange
        string = "Wir suchen eine Coiffeuse welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Coiffeur'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Coiffeuse', {'...chen eine Coiffeuse welche ge...'})
        ))

    def test_find_matches_search_male_finds_female_forms_frau(self):
        # arrange
        string = "Wir suchen eine Kauffrau welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Kaufmann'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Kauffrau', {'...chen eine Kauffrau welche ge...'})
        ))

    def test_find_matches_search_male_MANN_match_contains_male_slash_female(self):
        # Suche nach KaufMANN
        # arrange
        string = "Wir suchen eine(n) Kaufmann/-frau welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Kaufmann'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Kaufmann/-frau', {'...n eine(n) Kaufmann/-frau welche ge...'})
        ))

    def test_find_matches_search_FRAU_match_contains_male_slash_female(self):
        # Suche nach KaufFRAU
        # arrange
        string = "Wir suchen eine(n) Kaufmann/-frau welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Kauffrau'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Kaufmann/-frau', {'...n eine(n) Kaufmann/-frau welche ge...'})
        ))

    def test_find_matches_search_male_EUR_match_contains_male_slash_female(self):
        # Suche nach CoiffEUR
        # arrange
        string = "Wir suchen eine(n) Coiffeur/-euse welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Coiffeur'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Coiffeur/-euse', {'...n eine(n) Coiffeur/-euse welche ge...'})
        ))

    def test_find_matches_search_male_EUSE_match_contains_male_slash_female(self):
        # Suche nach CoiffEUSE
        # arrange
        string = "Wir suchen eine(n) Coiffeur/-euse welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Coiffeuse'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Coiffeur/-euse', {'...n eine(n) Coiffeur/-euse welche ge...'})
        ))

    def test_find_matches_search_male_ER_match_contains_male_slash_female(self):
        # Suche nach SchneidER
        # arrange
        string = "Wir suchen eine(n) Schreiner/-in welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Schreiner'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Schreiner/-in', {'...n eine(n) Schreiner/-in welche ge...'})
        ))

    def test_find_matches_search_male_ERIN_match_contains_male_slash_female(self):
        # Suche nach SchneidER
        # arrange
        string = "Wir suchen eine(n) Schreiner/-in welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Schreinerin'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Schreiner/-in', {'...n eine(n) Schreiner/-in welche ge...'})
        ))

    def test_find_matches_search_female_match_contains_male_slash_female(self):
        # Suche nach KaufFRAU, Coiffeur, Schreiner: Result Item enthält Kaufmann/-frau, Coiffeur/-euse, Schreiner/-in
        # arrange
        string = "Wir suchen eine(n) Kaufmann/-frau welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Kauffrau'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Kaufmann/-frau', {'...n eine(n) Kaufmann/-frau welche ge...'})
        ))

    def test_find_matches_search_male_match_contains_male_slash_female(self):
        # Suche nach Kaufmann, Coiffeur, Schreiner: Result Item enthält Kaufmann/-frau, Coiffeur/-euse, Schreiner/-in
        # arrange
        string = "Wir suchen eine(n) Kaufmann/-frau welche gerne arbeitet"
        # act
        result = testee.find_matches(string, ['Kauffrau'])
        # assert
        assert_that(result, only_contains(
            result_item_with_name_and_context('Kaufmann/-frau', {'...n eine(n) Kaufmann/-frau welche ge...'})
        ))

    @unittest.skip("to do")
    def test_find_matches_search_female_finds_male_forms(self):
        pass

    @unittest.skip("to do")
    def test_find_matches_finds_plurals(self):
        pass

    @unittest.skip("to do")
    def test_find_matches_finds_hypenated(self):
        pass

    @unittest.skip("to do")
    def test_find_matches_includes_brackets_mw(self):
        pass

    def test_determine_context_token_simple_returns_token(self):
        # act
        str = 'bla Schreiner bla'
        match_obj = re.search('Schreiner', str)
        # arrange
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_('Schreiner'))

    def test_determine_context_token_fm_slash_in_returns_token_slash_in(self):
        # arrange
        str = 'bla Schreiner/-in bla'
        match_obj = re.search('Schreiner', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Schreiner/-in"))

    def test_determine_context_token_fm_slash_euse_returns_token_slash_euse(self):
        # arrange
        str = 'bla Coiffeur/-euse bla'
        match_obj = re.search('Coiffeur', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Coiffeur/-euse"))

    def test_determine_context_token_fm_slash_frau_returns_token_slash_frau(self):
        # arrange
        str = 'bla Kaufmann/-frau bla'
        match_obj = re.search('Kaufmann', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Kaufmann/-frau"))

    def test_determine_context_token_fm_in_returns_token_slash_in(self):
        # arrange
        str = 'bla Schreinerin bla'
        match_obj = re.search('Schreiner', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Schreinerin"))

    def test_determine_context_token_fm_euse_returns_token_slash_euse(self):
        # arrange
        str = 'bla Coiffeuse bla'
        match_obj = re.search('Coiff(eur|euse)', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Coiffeuse"))

    def test_determine_context_token_fm_frau_returns_token_slash_frau(self):
        # arrange
        str = 'bla Kauffrau bla'
        match_obj = re.search('Kauf(mann|frau)', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_("Kauffrau"))

    def test_determine_context_token_mw_returns_token_including_mw(self):
        # arrange
        str = 'bla Sachbearbeiter (m/w) bla'
        match_obj = re.search('Sachbearbeiter', str)
        # act
        result = testee.determine_context_token(str, match_obj)
        # assert
        assert_that(result, is_('Sachbearbeiter (m/w)'))

    def test_to_male_form_returns_male_form(self):
        assert_that(testee.to_male_form("Schreinerin"), is_("Schreiner"))
        assert_that(testee.to_male_form("Coiffeuse"), is_("Coiffeur"))
        assert_that(testee.to_male_form("Kauffrau"), is_("Kaufmann"))

    def test_to_female_form_returns_female_form(self):
        assert_that(testee.to_female_form("Schreiner"), is_("Schreinerin"))
        assert_that(testee.to_female_form("Coiffeur"), is_("Coiffeuse"))
        assert_that(testee.to_female_form("Kaufmann"), is_("Kauffrau"))


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
