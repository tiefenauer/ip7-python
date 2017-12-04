import unittest

from hamcrest import assert_that, is_, contains, less_than

from src.classifier.jobtitle import jobtitle_structural_classifier_nvt
from src.classifier.jobtitle.jobtitle_structural_classifier_nvt import JobtitleStructuralClassifierNVT
from src.preprocessing.structural_preprocessor_nvt import StructuralPreprocessorNVT
from test.util.test_util import create_dummy_args

args = create_dummy_args()
preprocessor = StructuralPreprocessorNVT()
testee = JobtitleStructuralClassifierNVT(args, preprocessor)


class TestStructuralClassifierNVT(unittest.TestCase):
    def test_compare_tags(self):
        assert_that(jobtitle_structural_classifier_nvt.compare_tag('h1', 'h2'), is_(less_than(0)))
        assert_that(jobtitle_structural_classifier_nvt.compare_tag('h2', 'h3'), is_(less_than(0)))
        assert_that(jobtitle_structural_classifier_nvt.compare_tag('h3', 'h4'), is_(less_than(0)))
        assert_that(jobtitle_structural_classifier_nvt.compare_tag('h1', 'p'), is_(less_than(0)))
        assert_that(jobtitle_structural_classifier_nvt.compare_tag('h2', 'p'), is_(less_than(0)))
        assert_that(jobtitle_structural_classifier_nvt.compare_tag('h3', 'p'), is_(less_than(0)))
        assert_that(jobtitle_structural_classifier_nvt.compare_tag('h4', 'p'), is_(less_than(0)))

    def test_get_higher_tag(self):
        assert_that(jobtitle_structural_classifier_nvt.get_higher_tag('h1', 'h2'), is_('h1'))
        assert_that(jobtitle_structural_classifier_nvt.get_higher_tag('h2', 'h3'), is_('h2'))
        assert_that(jobtitle_structural_classifier_nvt.get_higher_tag('h3', 'h4'), is_('h3'))
        assert_that(jobtitle_structural_classifier_nvt.get_higher_tag('h1', 'p'), is_('h1'))
        assert_that(jobtitle_structural_classifier_nvt.get_higher_tag('h2', 'p'), is_('h2'))
        assert_that(jobtitle_structural_classifier_nvt.get_higher_tag('h3', 'p'), is_('h3'))
        assert_that(jobtitle_structural_classifier_nvt.get_higher_tag('h4', 'p'), is_('h4'))

    def test_top_n_returns_top_n(self):
        # arrange
        tagged_words = [
            # 6x noun1
            ('noun1', 'NN', 'h1'),
            ('noun1', 'NN', 'h2'),
            ('noun1', 'NN', 'h3'),
            ('noun1', 'NN', 'h4'),
            ('noun1', 'NN', 'p'),
            ('noun1', 'NN', 'p'),
            # 5x noun2
            ('noun2', 'NN', 'h2'),
            ('noun2', 'NN', 'h3'),
            ('noun2', 'NN', 'h4'),
            ('noun2', 'NN', 'p'),
            ('noun2', 'NN', 'p'),
            # 4x noun3
            ('noun3', 'NN', 'h3'),
            ('noun3', 'NN', 'h4'),
            ('noun3', 'NN', 'p'),
            ('noun3', 'NN', 'p'),
            # 3x noun4
            ('noun4', 'NN', 'h3'),
            ('noun4', 'NN', 'h4'),
            ('noun4', 'NN', 'p'),
            # 2x noun5
            ('noun5', 'NN', 'h4'),
            ('noun5', 'NN', 'p'),
            # 1x noun5
            ('noun6', 'NN', 'p'),

            # 6x verb1
            ('verb1', 'VVFIN', 'h1'),
            ('verb1', 'VVIMP', 'h2'),
            ('verb1', 'VVIZU', 'h3'),
            ('verb1', 'VVFIN', 'h4'),
            ('verb1', 'VMPP', 'p'),
            ('verb1', 'VVFIN', 'p'),
            # 5x verb2
            ('verb2', 'VMINF', 'h2'),
            ('verb2', 'VVFIN', 'h3'),
            ('verb2', 'VVIZU', 'h4'),
            ('verb2', 'VVFIN', 'p'),
            ('verb2', 'VVFIN', 'p'),
            # 4x verb3
            ('verb3', 'VVFIN', 'h3'),
            ('verb3', 'VMINF', 'h4'),
            ('verb3', 'VVFIN', 'p'),
            ('verb3', 'VVFIN', 'p'),
            # 3x verb4
            ('verb4', 'VVIZU', 'h4'),
            ('verb4', 'VVFIN', 'p'),
            ('verb4', 'VMPP', 'p'),
            # 2x verb5
            ('verb5', 'VVIZU', 'p'),
            ('verb5', 'VMPP', 'p'),
            # 1x verb6
            ('verb6', 'VMPP', 'p'),
        ]
        # act
        result = jobtitle_structural_classifier_nvt.top_n(tagged_words, 'N', 3)
        # assert
        assert_that(result, contains(
            ('noun1', 'h1', 6),  # noun1 with highest tag h1 and occurrence 6
            ('noun2', 'h2', 5),  # noun1 with highest tag h2 and occurrence 5
            ('noun3', 'h3', 4)  # noun1 with highest tag h3 and occurrence 4
        ))

    def test_extract_features(self):
        # arrange
        tagged_words = [
            ('Baumeister', 'NN', 'h1'),
            ('Auto', 'NN', 'h2'),
            ('Maler', 'NN', 'h3'),
            ('Bäcker', 'NN', 'h4'),
            ('Fahrrad', 'NN', 'p'),
            ('sehen', 'V', 'h1'),
            ('backen', 'V', 'h2'),
            ('braten', 'V', 'h3'),
            ('kochen', 'V', 'h4'),
            ('suchen', 'V', 'div')
        ]
        # act
        features = testee.extract_features(tagged_words)
        # assert
        assert_that(features['N-word-1'], is_('Baumeister'))
        assert_that(features['N-tag-1'], is_('h1'))

        assert_that(features['N-word-2'], is_('Auto'))
        assert_that(features['N-tag-2'], is_('h2'))

        assert_that(features['N-word-3'], is_('Maler'))
        assert_that(features['N-tag-3'], is_('h3'))

        assert_that(features['N-word-4'], is_('Bäcker'))
        assert_that(features['N-tag-4'], is_('h4'))

        assert_that(features['N-word-5'], is_('Fahrrad'))
        assert_that(features['N-tag-5'], is_('p'))

        assert_that(features['V-word-1'], is_('sehen'))
        assert_that(features['V-tag-1'], is_('h1'))

        assert_that(features['V-word-2'], is_('backen'))
        assert_that(features['V-tag-2'], is_('h2'))

        assert_that(features['V-word-3'], is_('braten'))
        assert_that(features['V-tag-3'], is_('h3'))

        assert_that(features['V-word-4'], is_('kochen'))
        assert_that(features['V-tag-4'], is_('h4'))

        assert_that(features['V-word-5'], is_('suchen'))
        assert_that(features['V-tag-5'], is_('div'))
