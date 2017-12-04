import unittest

import bs4
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

from src.classifier.jobtitle import jobtitle_fts_classifier_htmltag_based as clf_htmltag_based
from src.classifier.jobtitle.jobtitle_fts_classifier_htmltag_based import FeatureBasedJobtitleFtsClassifier
from src.util.jobtitle_util import create_gender_variants
from test.util.test_util import create_dummy_args


def create_tag(tag_name, tag_content):
    tag = bs4.BeautifulSoup('', 'html.parser').new_tag(tag_name)
    tag.string = tag_content
    return tag


def feature_matching(job_name, variant_name, tag_name, count):
    return FeatureMatcher(job_name, variant_name, tag_name, count)


class FeatureMatcher(BaseMatcher):
    def __init__(self, job_name, variant_name, tag_name, count):
        self.job_name = job_name
        self.variant_name = variant_name
        self.tag_name = tag_name
        self.count = count

    def _matches(self, item):
        return self.job_name in item \
               and self.variant_name in item[self.job_name] \
               and self.tag_name in item[self.job_name][self.variant_name] \
               and item[self.job_name][self.variant_name][self.tag_name] == self.count

    def describe_to(self, description):
        description.append_text('feature matching job_name=\'') \
            .append_text(self.job_name) \
            .append_text(' and tag_name=') \
            .append_text(self.tag_name) \
            .append_text(' and count=') \
            .append_text(self.count) \
            .append_text('\'')


def create_job_name_tuple(*job_names):
    for job_name in job_names:
        yield job_name, create_gender_variants(job_name)


args = create_dummy_args()
testee = FeatureBasedJobtitleFtsClassifier(args)


class TestFeatureBasedJobtitleFtsClassifier(unittest.TestCase):
    def test_classify_one_tag_one_job_one_variant_returns_correct_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Wir suchen eine/n Polymechaniker/-in mit Freude an der Arbeit.')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Polymechaniker/-in'))

    def test_classify_one_tag_one_job_multi_variants_returns_longer_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Polymechaniker/-in Polymechaniker')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Polymechaniker/-in'))

    def test_classify_one_tag_one_job_multi_variants_returns_most_frequent_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Polymechaniker/-in Polymechaniker Polymechaniker')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Polymechaniker'))

    def test_classify_one_tag_multi_jobs_one_variant_returns_most_frequent_job(self):
        # arrange
        tags = [
            create_tag('h1', 'Koch Koch Polymechaniker Polymechaniker Polymechaniker Priester'),
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Polymechaniker'))

    def test_classify_one_tag_multi_jobs_multi_variants_returns_most_frequent_job_longest_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Koch Priester Priester/in'),
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Priester/in'))

    def test_classify_one_tag_multi_jobs_multi_variants_returns_most_frequent_job_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Koch Priester Priester Priester/in'),
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Priester'))

    def test_classify_multi_tag_one_tagtype_one_job_one_variant_returns_correct_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Coiffeur'),
            create_tag('h1', 'Coiffeur')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Coiffeur'))

    def test_classify_multi_tag_one_tagtype_one_job_multi_variants_returns_longer_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Coiffeur'),
            create_tag('h1', 'Coiffeuse')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Coiffeuse'))

    def test_classify_multi_tag_multi_tagtype_one_job_multi_variants_returns_higher_ranked_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Coiffeur'),
            create_tag('h2', 'Coiffeuse')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Coiffeur'))

    def test_classify_multi_tag_one_tagtype_one_job_multi_variants_returns_most_frequent_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Coiffeur Coiffeuse'),
            create_tag('h1', 'Coiffeuse')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Coiffeuse'))

    def test_classify_multi_tag_one_tagtype_multi_job_one_variant_result_is_most_frequent_job(self):
        # arrange
        tags = [
            create_tag('h1', 'Koch Koch Priester'),
            create_tag('h1', 'Priester Priester')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Priester'))

    def test_classify_multi_tag_one_tagtype_multi_job_multi_variants_result_is_most_frequent_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Koch Koch Priester/in'),
            create_tag('h1', 'Priester/in Priester')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Priester/in'))

    def test_classify_multi_tag_one_tagtype_multi_job_multi_variants_result_is_longest_variant(self):
        # arrange
        tags = [
            create_tag('h1', 'Koch Koch Priester/-in'),
            create_tag('h1', 'Priester/in Priester')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Priester/-in'))

    def test_classify_multi_tag_one_tagtype_multi_job_multi_variant_result_is_the_one_with_more_diversity(self):
        # arrange
        tags = [
            create_tag('h1', 'Koch Koch Koch'),
            create_tag('h1', 'Priester Priester/in Priester/in')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Priester/in'))

    def test_classify_multi_tag_multi_job_result_is_the_one_with_lower_tag(self):
        # arrange
        tags = [
            create_tag('h2', 'Coiffeur'),
            create_tag('h1', 'Polymechaniker/in')
        ]
        # act
        result = testee.classify(tags)
        # assert
        assert_that(result, is_('Polymechaniker/in'))

    def test_extract_features_no_match_returns_empty_list(self):
        # arrange
        tags = [create_tag('p', 'nothing to see here...')]
        jnv = create_job_name_tuple('Polymechaniker', 'Priester', 'Koch')
        # act
        features = clf_htmltag_based.extract_features(tags, jnv)
        # assert
        assert_that(features, is_({}))

    def test_extract_features_from_one_tag_one_match(self):
        # arrange
        tags = [create_tag('h2', 'Wir suchen einen Polymechaniker (m/w) der gerne arbeitet')]
        jnv = create_job_name_tuple('Polymechaniker')
        # act
        features = clf_htmltag_based.extract_features(tags, jnv)
        # assert
        assert_that(features, is_(feature_matching('Polymechaniker', 'Polymechaniker (m/w)', 'h2', 1)))

    def test_extract_features_from_one_tag_multi_match(self):
        # arrange
        tags = [create_tag('h2', 'Koch (m/w) Polymechaniker Polymechaniker/in Polymechaniker Priester Priester/-in')]
        jnv = create_job_name_tuple('Polymechaniker', 'Priester', 'Koch')
        # act
        features = clf_htmltag_based.extract_features(tags, jnv)
        # assert
        assert_that(features, is_(feature_matching('Polymechaniker', 'Polymechaniker', 'h2', 2)))
        assert_that(features, is_(feature_matching('Polymechaniker', 'Polymechaniker/in', 'h2', 1)))
        assert_that(features, is_(feature_matching('Priester', 'Priester', 'h2', 1)))
        assert_that(features, is_(feature_matching('Priester', 'Priester/-in', 'h2', 1)))
        assert_that(features, is_(feature_matching('Koch', 'Koch (m/w)', 'h2', 1)))

    def test_extract_features_from_multi_tag_one_match(self):
        # arrange
        tags = [
            create_tag('h2', 'Polymechaniker'),
            create_tag('h2', 'Polymechaniker')
        ]
        jnv = create_job_name_tuple('Polymechaniker')
        # act
        features = clf_htmltag_based.extract_features(tags, jnv)
        # assert
        assert_that(features, is_(feature_matching('Polymechaniker', 'Polymechaniker', 'h2', 2)))

    def test_extract_features_from_multi_different_tag_one_match(self):
        # arrange
        tags = [
            create_tag('h1', 'Polymechaniker'),
            create_tag('h2', 'Polymechaniker/-in')
        ]
        jnv = create_job_name_tuple('Polymechaniker', 'Priester', 'Koch')
        # act
        features = clf_htmltag_based.extract_features(tags, jnv)
        # assert
        assert_that(features, is_(feature_matching('Polymechaniker', 'Polymechaniker', 'h1', 1)))
        assert_that(features, is_(feature_matching('Polymechaniker', 'Polymechaniker/-in', 'h2', 1)))

    def test_extract_features_from_multi_tag_multi_match(self):
        # arrange
        tags = [
            create_tag('h1', 'Polymechaniker'),
            create_tag('h2', 'Koch (m/w)')
        ]
        jnv = create_job_name_tuple('Polymechaniker', 'Koch')
        # act
        features = clf_htmltag_based.extract_features(tags, jnv)
        # assert
        assert_that(features, is_(feature_matching('Polymechaniker', 'Polymechaniker', 'h1', 1)))
        assert_that(features, is_(feature_matching('Koch', 'Koch (m/w)', 'h2', 1)))

    def test_calc_score_calculates_correct_score(self):
        assert_that(clf_htmltag_based.calculate_score('h1', 1), is_(0.6))
        assert_that(clf_htmltag_based.calculate_score('h2', 1), is_(0.3))
        assert_that(clf_htmltag_based.calculate_score('h2', 2), is_(0.6))
        assert_that(clf_htmltag_based.calculate_score('p', 1), is_(0.1))

    def test_normalize_returns_score_between_0_and_1(self):
        assert_that(clf_htmltag_based.normalize(0.6), is_(0.6))
        assert_that(clf_htmltag_based.normalize(1.2), is_(1 / 1.2))

    def test_count_variants_returns_correct_job(self):
        # arrange
        tag = 'Polymechaniker'
        # act
        result = clf_htmltag_based.count_variants(tag, create_gender_variants('Polymechaniker'))
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1)
        ))

    def test_count_variants_with_variant_slash_hyphen_in_returns_correct_job_title(self):
        # arrange
        tag = 'Polymechaniker/-in'
        # act
        result = clf_htmltag_based.count_variants(tag, create_gender_variants('Polymechaniker'))
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker/-in', 1)
        ))

    def test_count_variants_with_variant_slash_hyphen_euse_returns_correct_job_title(self):
        # arrange
        tag = 'Coiffeur/-euse'
        # act
        result = clf_htmltag_based.count_variants(tag, create_gender_variants('Coiffeur'))
        # assert
        assert_that(result, contains_inanyorder(
            ('Coiffeur/-euse', 1)
        ))

    def test_count_variants_with_variant_slash_hyphen_frau_returns_correct_job_title(self):
        # arrange
        tag = 'Kaufmann/-frau'
        # act
        result = clf_htmltag_based.count_variants(tag, create_gender_variants('Kaufmann'))
        # assert
        assert_that(result, contains_inanyorder(
            ('Kaufmann/-frau', 1)
        ))

    def test_count_variants_with_variant_slash_in_returns_correct_job_title(self):
        # arrange
        tag = 'Polymechaniker/in'
        # act
        result = clf_htmltag_based.count_variants(tag, create_gender_variants('Polymechaniker'))
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker/in', 1)
        ))

    def test_count_variants_with_variant_slash_euse_returns_correct_job_title(self):
        # arrange
        tag = 'Coiffeur/euse'
        # act
        result = clf_htmltag_based.count_variants(tag, create_gender_variants('Coiffeur'))
        # assert
        assert_that(result, contains_inanyorder(
            ('Coiffeur/euse', 1)
        ))

    def test_count_variants_with_variant_slash_frau_returns_correct_job_title(self):
        # arrange
        tag = 'Kaufmann/frau'
        # act
        result = clf_htmltag_based.count_variants(tag, create_gender_variants('Kaufmann'))
        # assert
        assert_that(result, contains_inanyorder(
            ('Kaufmann/frau', 1)
        ))

    def test_count_variants_with_variant_mw_returns_correct_job_title(self):
        # arrange
        string = 'Polymechaniker (m/w)'
        # act
        result = clf_htmltag_based.count_variants(string, create_gender_variants('Polymechaniker'))
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker (m/w)', 1)
        ))

    def test_count_variants_multi_returns_correct_job_count(self):
        # arrange
        string = '<h2>Polymechaniker oder Polymechanikerin</h2>'
        # act
        result = clf_htmltag_based.count_variants(string, create_gender_variants('Polymechaniker'))
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1),
            ('Polymechanikerin', 1)
        ))

    def test_count_variants_multi_variants_returns_correct_job_count(self):
        # arrange
        tag = 'Coiffeur/-euse, Polymechaniker/in, Kaufmann (m/w)'
        variants = create_gender_variants('Polymechaniker') \
            .union(create_gender_variants('Coiffeur')) \
            .union(create_gender_variants('Kaufmann'))
        # act
        result = clf_htmltag_based.count_variants(tag, variants)
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker/in', 1),
            ('Coiffeur/-euse', 1),
            ('Kaufmann (m/w)', 1)
        ))
