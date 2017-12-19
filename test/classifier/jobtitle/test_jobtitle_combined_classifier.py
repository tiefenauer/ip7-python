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

    def test_find_job_without_match_returns_None(self):
        # arrange
        job_name = 'Bäcker'
        sentence = 'Wir suchen einen Geschäftsführer'
        # act
        result = jobtitle_combined_classifier.find_job(job_name, sentence)
        assert_that(result, is_(None))

    def test_find_job_with_simple_name_returns_exact_match(self):
        # arrange
        job_name = 'Polymechaniker'
        sentence = 'Wir suchen einen Polymechaniker'
        # act
        result = jobtitle_combined_classifier.find_job(job_name, sentence)
        assert_that(result, is_('Polymechaniker'))

    def test_find_job_with_compound_name_returns_compound_name(self):
        # arrange
        job_name = 'Compliance Officer'
        sentence = 'Wir suchen einen Compliance Officer mit Erfahrung'
        # act
        result = jobtitle_combined_classifier.find_job(job_name, sentence)
        assert_that(result, is_('Compliance Officer'))

    def test_find_job_with_expandable_job_name_returns_expandable_job_name(self):
        # arrange
        job_name_1 = 'Polymechaniker'
        job_name_2 = 'CNC Fräser'
        sentence = 'Polymechaniker / CNC Fräser 80% - 100% (m/w)'
        # act
        result_1 = jobtitle_combined_classifier.find_job(job_name_1, sentence)
        result_2 = jobtitle_combined_classifier.find_job(job_name_2, sentence)
        assert_that(result_1, is_('Polymechaniker / CNC Fräser'))
        assert_that(result_2, is_('Polymechaniker / CNC Fräser'))

    def test_find_job_with_expandable_compound_job_name_returns_expandable_job_name(self):
        # arrange
        job_name = 'Compliance Officer'
        sentence = 'Team Head Compliance Officer Premium Clients Switzerland (80-100%)'
        # act
        result = jobtitle_combined_classifier.find_job(job_name, sentence)
        assert_that(result, is_('Team Head Compliance Officer Premium Clients Switzerland'))

    def test_to_sentences_map_one_sentence_returns_map_tag_name_sentences(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Wir suchen einen Geschäftsführer.'),
            create_tag('h2', 'Willst du dich bewerben?'),
            create_tag('p', 'Erfahrung wird überbewertet!')
        ]
        # act
        result = jobtitle_combined_classifier.to_sentences_map(html_tags)
        result = list(result)
        # asser
        assert_that(result, only_contains(
            ('h1', 'Wir suchen einen Geschäftsführer.'),
            ('h2', 'Willst du dich bewerben?'),
            ('p', 'Erfahrung wird überbewertet!')
        ))

    def test_to_sentences_map_multi_sentence_returns_one_entry_per_sentence(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Wir suchen einen Geschäftsführer. Willst du dich bewerben?'),
            create_tag('p', 'Erfahrung wird überbewertet!')
        ]
        # act
        result = jobtitle_combined_classifier.to_sentences_map(html_tags)
        result = list(result)
        # asser
        assert_that(result, only_contains(
            ('h1', 'Wir suchen einen Geschäftsführer.'),
            ('h1', 'Willst du dich bewerben?'),
            ('p', 'Erfahrung wird überbewertet!')
        ))

    def test_calculate_positions_with_exact_match(self):
        # arrange
        job_name_tokenized = preproc.to_words('Erzieher')
        sentence_tokenized = preproc.to_words('Erzieher / Gruppenleitung')
        # act
        result = jobtitle_combined_classifier.calculate_positions(job_name_tokenized, sentence_tokenized)
        assert_that(result, is_((0, 1)))

    def test_calculate_positions_with_fuzzy_match(self):
        # arrange
        job_name_tokenized = preproc.to_words('Erzieher')
        sentence_tokenized = preproc.to_words('Erzieherin / Gruppenleitung')
        # act
        result = jobtitle_combined_classifier.calculate_positions(job_name_tokenized, sentence_tokenized)
        assert_that(result, is_((0, 1)))
