import unittest

from hamcrest import assert_that, is_

from src.classifier.jobtitle.jobtitle_combined_classifier import CombinedJobtitleClassifier
from src.preprocessing import preproc

testee = CombinedJobtitleClassifier()


def to_tagged_words(text):
    return preproc.pos_tag(preproc.to_words(text))


class TestCombinedJobtitleClassifier(unittest.TestCase):

    def test_predict_class_with_normal_hit(self):
        # arrange
        htmltag_sentence_map = [
            ('h2', 'Wir suchen einen Polymechaniker')
        ]
        # act
        result = testee.predict_class(htmltag_sentence_map)
        # assert
        assert_that(result, is_('Polymechaniker'))

    def test_predict_class_with_normal_hit_finds_hits_in_multiple_equal_tags(self):
        # arrange
        htmltag_sentence_map = [
            ('h2', 'Nothing to see here'),
            ('h2', 'Wir suchen einen Polymechaniker')
        ]
        # act
        result = testee.predict_class(htmltag_sentence_map)
        # assert
        assert_that(result, is_('Polymechaniker'))

    def test_predict_class_with_normal_hit_sorts_hits_by_tag_position(self):
        # arrange
        htmltag_sentence_map = [
            ('h2', 'Wir suchen einen Bäcker'),
            ('h2', 'Wir suchen einen Polymechaniker')
        ]
        # act
        result = testee.predict_class(htmltag_sentence_map)
        # assert
        assert_that(result, is_('Bäcker'))

    def test_predict_class_with_normal_hit_sorts_hits_by_tag_weight(self):
        # arrange
        htmltag_sentence_map = [
            ('h2', 'Wir suchen einen Bäcker'),
            ('h1', 'Wir suchen einen Polymechaniker')
        ]
        # act
        result = testee.predict_class(htmltag_sentence_map)
        # assert
        assert_that(result, is_('Polymechaniker'))

    def test_predict_class_with_improvable_hit(self):
        # arrange
        htmltag_sentence_map = [
            ('h2', 'Polymechaniker / CNC Fräser 80% - 100% (m/w)')
        ]
        # act
        result = testee.predict_class(htmltag_sentence_map)
        # assert
        assert_that(result, is_('Polymechaniker / CNC Fräser'))

    def test_predict_class_with_compound_hit(self):
        # arrange
        htmltag_sentence_map = [
            ('h2', 'Team Head Compliance Officer Premium Clients Switzerland (80-100%)')
        ]
        # act
        result = testee.predict_class(htmltag_sentence_map)
        # assert
        assert_that(result, is_('Team Head Compliance Officer Premium Clients Switzerland'))

