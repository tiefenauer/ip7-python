import unittest

from hamcrest import assert_that, only_contains, is_, contains_inanyorder
from hamcrest.core.base_matcher import BaseMatcher

from src.jobtitle import jobtitle_matcher as testee


class TestJobTitleMatcher(unittest.TestCase):
    def test_to_male_form_returns_male_form(self):
        assert_that(testee.to_male_form("Schreinerin"), is_("Schreiner"))
        assert_that(testee.to_male_form("Coiffeuse"), is_("Coiffeur"))
        assert_that(testee.to_male_form("Kauffrau"), is_("Kaufmann"))

    def test_to_female_form_returns_female_form(self):
        assert_that(testee.to_female_form("Schreiner"), is_("Schreinerin"))
        assert_that(testee.to_female_form("Coiffeur"), is_("Coiffeuse"))
        assert_that(testee.to_female_form("Kaufmann"), is_("Kauffrau"))

    def test_to_slashed_form_returns_hyphenated(self):
        assert_that(testee.to_slashed_form('Schreiner'), is_('Schreiner/in'))
        assert_that(testee.to_slashed_form('Coiffeur'), is_('Coiffeur/euse'))
        assert_that(testee.to_slashed_form('Kaufmann'), is_('Kaufmann/frau'))

    def test_to_slashed_hyphen_form_returns_slashed_hyphen(self):
        assert_that(testee.to_slashed_hyphen_form('Schreiner'), is_('Schreiner/-in'))
        assert_that(testee.to_slashed_hyphen_form('Coiffeur'), is_('Coiffeur/-euse'))
        assert_that(testee.to_slashed_hyphen_form('Kaufmann'), is_('Kaufmann/-frau'))

    def test_to_mw_form_returns_mw_form(self):
        assert_that(testee.to_mw_form('Schreinerin'), is_('Schreiner (m/w)'))
        assert_that(testee.to_mw_form('Coiffeuse'), is_('Coiffeur (m/w)'))
        assert_that(testee.to_mw_form('Kauffrau'), is_('Kaufmann (m/w)'))

    def test_find_single_match(self):
        # arrange / act
        result = testee.find('Wir suchen einen 20-jährigen Schreiner mit 30 Jahren Erfahrung', 'Schreiner')
        # assert
        assert_that(result, only_contains(
            match_item_for_job_name('Schreiner')
        ))

    def test_find_suffix_in(self):
        # arrange/act
        result_m = testee.find("Wir suchen eine Schreinerin welche gerne arbeitet", 'Schreiner')
        # assert
        assert_that(result_m, only_contains(match_item_for_job_name('Schreinerin')))

    def test_find_suffix_euse(self):
        # arrange/act
        result = testee.find('Wir suchen eine Coiffeuse welche gerne arbeitet', 'Coiffeur')
        # assert
        assert_that(result, only_contains(match_item_for_job_name('Coiffeuse')))

    def test_find_suffix_frau(self):
        # arrange/act
        result = testee.find('Wir suchen eine Kauffrau welche gerne arbeitet', 'Kaufmann')
        # assert
        assert_that(result, only_contains(match_item_for_job_name('Kauffrau')))

    def test_find_slashed_in(self):
        # arrange/act
        result_hyphen = testee.find('Wir suchen eine(n) Schreiner/-in welche gerne arbeitet', 'Schreiner')
        result_no_hypen = testee.find('Wir suchen eine(n) Schreiner/in welche gerne arbeitet', 'Schreiner')
        # assert
        assert_that(result_hyphen, only_contains(match_item_for_job_name('Schreiner/-in')))
        assert_that(result_no_hypen, only_contains(match_item_for_job_name('Schreiner/in')))

    def test_find_slashed_euse(self):
        # arrange/act
        result_hyphen = testee.find('Wir suchen eine(n) Coiffeur/-euse welche gerne arbeitet', 'Coiffeur')
        result_no_hyphen = testee.find('Wir suchen eine(n) Coiffeur/euse welche gerne arbeitet', 'Coiffeur')
        # assert
        assert_that(result_hyphen, only_contains(match_item_for_job_name('Coiffeur/-euse')))
        assert_that(result_no_hyphen, only_contains(match_item_for_job_name('Coiffeur/euse')))

    def test_find_slashed_frau(self):
        # arrange/act
        result_hyphen = testee.find('Wir suchen eine(n) Kaufmann/-frau welche gerne arbeitet', 'Kaufmann')
        result_no_hypen = testee.find('Wir suchen eine(n) Kaufmann/frau welche gerne arbeitet', 'Kaufmann')
        # assert
        assert_that(result_hyphen, only_contains(match_item_for_job_name('Kaufmann/-frau')))
        assert_that(result_no_hypen, only_contains(match_item_for_job_name('Kaufmann/frau')))

    def test_find_multiple_match(self):
        # arrange/act
        result = testee.find('Wir suchen einen Schreiner oder eine Schreinerin, der bei uns arbeitet', 'Schreiner')
        # assert
        assert_that(result, only_contains(
            match_item_for_job_name('Schreiner'),
            match_item_for_job_name('Schreinerin')
        ))

    def test_create_search_group_returns_search_group(self):
        # arrange
        job_name = 'Schreiner'
        # act
        result = testee.create_search_group(job_name)
        # assert
        assert_that(result, contains_inanyorder('Schreiner',
                                                'Schreinerin',
                                                'Schreiner/-in',
                                                'Schreiner/in',
                                                'Schreiner (m/w)'
                                                )
                    )

    def test_create_search_group_does_not_contain_duplicates(self):
        # arrange
        job_name = "Koch"
        # act
        result = testee.create_search_group(job_name)
        assert_that(result, contains_inanyorder('Koch', 'Koch (m/w)'), "For job names with no easy female form do not return duplicates")


def match_item_for_job_name(job_name):
    return IsMatchItemForJobName(job_name)


class IsMatchItemForJobName(BaseMatcher):
    def __init__(self, job_name):
        self.job_name = job_name

    def _matches(self, item):
        return item.group() == self.job_name

    def describe_to(self, description):
        description.append_text('match item with group matching \'') \
            .append_text(self.job_name) \
            .append_text('\'')
