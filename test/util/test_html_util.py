import unittest

from bs4 import BeautifulSoup, NavigableString
from hamcrest import *

from src.util import html_util


def create_tag(markup):
    soup = BeautifulSoup(markup, 'html.parser')
    return list(soup.children)[0]


class TestHtmlParser(unittest.TestCase):
    def test_is_relevant_with_relevant_tag_returns_true(self):
        # arrange
        tag_p = create_tag('<p></p>')
        tag_div = create_tag('<div></div>')
        tag_div_nested = create_tag('<div><img /></div>')
        # act/assert
        assert_that(html_util.is_relevant(tag_p), is_(not_(None)))
        assert_that(html_util.is_relevant(tag_div), is_(not_(None)))
        assert_that(html_util.is_relevant(tag_div_nested), is_(not_(None)))

    def test_is_relevant_with_irrelevant_tag_returns_false(self):
        # arrange
        tag_img = create_tag('<img/>')
        tag_form = create_tag('<form></form>')
        # act/assert
        assert_that(html_util.is_relevant(tag_img), is_(False))
        assert_that(html_util.is_relevant(tag_form), is_(False))

    def test_remove_all_attributes_without_whitelist_removes_all_attributes(self):
        # arrange
        tag = create_tag('<span lang="de" xml:lang="de">Kontakt</span>')
        # act
        tag = html_util.remove_all_attrs(tag)
        # assert
        assert_that(str(tag), is_('<span>Kontakt</span>'))
        assert_that(tag.attrs, is_(empty()))

    def test_strip_tag_without_inner_markup_returns_only_text(self):
        # arrange
        element = create_tag('<p>\r\n       foo             \r\n</p>')
        # act
        result = html_util.strip_content(element)
        # assert
        assert_that(str(result), equal_to('<p>foo</p>'))

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
        element_with_relevant_children = create_tag(markup)
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
        element_with_relevant_children = create_tag(markup)
        # act
        result = html_util.is_nested(element_with_relevant_children)
        # assert
        assert_that(result, is_(True))
