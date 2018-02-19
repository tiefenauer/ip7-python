import unittest

from bs4 import BeautifulSoup, NavigableString
from hamcrest import *

from src.preprocessing import preproc
from src.util import html_util


class TestHtmlParser(unittest.TestCase):
    def test_is_relevant_with_relevant_tag_returns_true(self):
        # arrange
        tag_p = preproc.create_tag_from_markup('<p></p>')
        tag_div = preproc.create_tag_from_markup('<div></div>')
        tag_div_nested = preproc.create_tag_from_markup('<div><img /></div>')
        # act/assert
        assert_that(html_util.is_relevant(tag_p), is_(not_(None)))
        assert_that(html_util.is_relevant(tag_div), is_(not_(None)))
        assert_that(html_util.is_relevant(tag_div_nested), is_(not_(None)))

    def test_is_relevant_with_irrelevant_tag_returns_false(self):
        # arrange
        tag_img = preproc.create_tag_from_markup('<img/>')
        tag_form = preproc.create_tag_from_markup('<form></form>')
        # act/assert
        assert_that(html_util.is_relevant(tag_img), is_(False))
        assert_that(html_util.is_relevant(tag_form), is_(False))

    def test_remove_all_attributes_without_whitelist_removes_all_attributes(self):
        # arrange
        tag = preproc.create_tag_from_markup('<span lang="de" xml:lang="de">Kontakt</span>')
        # act
        tag = html_util.remove_all_attrs(tag)
        # assert
        assert_that(str(tag), is_('<span>Kontakt</span>'))
        assert_that(tag.attrs, is_(empty()))

    def test_strip_tag_without_inner_markup_returns_only_text(self):
        # arrange
        element = preproc.create_tag_from_markup('<p>\r\n       foo             \r\n</p>')
        # act
        result = html_util.strip_content(element)
        # assert
        assert_that(str(result), is_('<p>foo</p>'))

    def test_contains_children_without_children_attribute_returns_false(self):
        # arrange
        tag = object()
        # act
        result = html_util.contains_children(tag)
        # assert
        assert_that(result, is_(False))

    def test_contains_children_with_children_attribute_empty_list_returns_false(self):
        # arrange
        element = NavigableString('foo')
        # act
        result = html_util.contains_children(element)
        # assert
        assert_that(result, is_(False))

    def test_contains_children_with_children_attribute_not_empty_list_returns_false(self):
        # arrange
        element = BeautifulSoup('<div><div>foo</div></div>', 'html.parser')
        # act
        result = html_util.contains_children(element)
        # assert
        assert_that(result, is_(True))

    def test_is_nested_without_relevant_children_returns_false(self):
        # arrange
        markup = """<form>
                        <img src="./foo.jpg"/>
                        <meta>
                            <!-- Nothing relevant here... -->
                            <input></input>
                        </meta>
                    </form>"""
        element_with_relevant_children = preproc.create_tag_from_markup(markup)
        # act
        result = html_util.is_nested(element_with_relevant_children)
        # assert
        assert_that(result, is_(False))

    def test_is_nested_with_relevant_children_returns_false(self):
        # arrange
        markup = """<div>
                        <img src="./foo.jpg"/>
                        <div>
                            <p>some relevant content</p>
                            <input></input>
                        </div>
                    </div>"""
        element_with_relevant_children = preproc.create_tag_from_markup(markup)
        # act
        result = html_util.is_nested(element_with_relevant_children)
        # assert
        assert_that(result, is_(True))

    def test_calculate_tag_weight_returns_correct_value(self):
        # arrange
        tags = [
            ('title', 'h1'),
            ('h1', 'h2'),
            ('h2', 'h3'),
            ('h3', 'h4'),
            ('h4', 'h5'),
            ('strong', 'p')
        ]
        # act / assert
        for more_important_tag, less_importand_tag in tags:
            higher_weight = html_util.calculate_tag_weight(more_important_tag)
            lower_weight = html_util.calculate_tag_weight(less_importand_tag)
            assert_that(higher_weight, is_(less_than(lower_weight)))
