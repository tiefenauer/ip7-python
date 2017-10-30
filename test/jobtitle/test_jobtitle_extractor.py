import unittest

from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

from src.jobtitle import jobtitle_extractor as testee


class TestJobTitleExtractor(unittest.TestCase):
    def test_extract_job_title_returns_correct_job(self):
        # arrange
        tag = '<h2>Polymechaniker</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1)
        ))

    def test_extract_job_title_with_variant_slash_hyphen_in_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Polymechaniker/-in</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1)
        ))

    def test_extract_job_title_with_variant_slash_hyphen_euse_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Coiffeur/-euse</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Coiffeur'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Coiffeur', 1)
        ))

    def test_extract_job_title_with_variant_slash_hyphen_frau_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Kaufmann/-frau</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Kaufmann', 1)
        ))

    def test_extract_job_title_with_variant_slash_in_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Polymechaniker/in</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1)
        ))

    def test_extract_job_title_with_variant_slash_euse_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Coiffeur/euse</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Coiffeur'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Coiffeur', 1)
        ))

    def test_extract_job_title_with_variant_slash_frau_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Kaufmann/frau</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Kaufmann', 1)
        ))

    def test_extract_job_title_with_variant_mw_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Polymechaniker (m/w)</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1)
        ))

    def test_extract_job_title_multi_returns_correct_job_count(self):
        # arrange
        tag = '<h2>Polymechaniker oder Polymechanikerin</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 2)
        ))

    def test_extract_job_title_multi_variants_returns_correct_job_count(self):
        # arrange
        tag = '<h2>Coiffeur/-euse, Polymechaniker/in, Kaufmann (m/w)</h2>'
        # act
        result = testee.extract_job_titles(tag, ['Polymechaniker', 'Coiffeur', 'Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1),
            ('Coiffeur', 1),
            ('Kaufmann', 1)
        ))

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

    def test_create_variants_returns_variants(self):
        # arrange
        job_name = 'Schreiner'
        # act
        result = testee.create_variants(job_name)
        # assert
        assert_that(result, contains_inanyorder('Schreiner',
                                                'Schreinerin',
                                                'Schreiner/-in',
                                                'Schreiner/in',
                                                'Schreiner (m/w)'
                                                )
                    )

    def test_create_variants_does_not_contain_duplicates(self):
        # arrange
        job_name = "Koch"
        # act
        result = testee.create_variants(job_name)
        assert_that(result, contains_inanyorder('Koch', 'Koch (m/w)'),
                    "For job names with no easy female form do not return duplicates")


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
