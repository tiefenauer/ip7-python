import unittest

from hamcrest import assert_that, is_, contains

from src.classifier.jobtitle import jobtitle_classifier_structural_nvt
from src.classifier.jobtitle.jobtitle_classifier_structural_nvt import JobtitleStructuralClassifierNVT
from test.testutils import create_dummy_args

args = create_dummy_args()
testee = JobtitleStructuralClassifierNVT(args)


class TestJobtitleStructuralClassifierNVT(unittest.TestCase):

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
        result = jobtitle_classifier_structural_nvt.top_n(tagged_words, 'N', 3)
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
        features = jobtitle_classifier_structural_nvt.extract_features(tagged_words)
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
