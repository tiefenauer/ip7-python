import unittest
from hamcrest import *
from src import html_extractor
from bs4 import BeautifulSoup, NavigableString, Tag


def read_sample_file(filename):
    with open('./resources/' + filename + '.html', 'r', encoding='utf-8') as file:
        return BeautifulSoup(file.read(), 'html.parser')


def write_extracted_tags(extracted_tags, filename):
    with open('./resources/' + filename + '_extracted.html', 'w+', encoding='utf-8') as file:
        for tag in extracted_tags:
            file.write(str(tag) + '\n')


def create_tag(markup):
    soup = BeautifulSoup(markup, 'html.parser')
    return list(soup.children)[0]


class TestHtmlParser(unittest.TestCase):
    def test_extract_tags_with_real_html_sample_returns_correct_extracted_tags(self):
        # arrange
        soup = read_sample_file('sample_vacancy')
        extracted_tags = []
        # act
        html_extractor.extract_tags(soup, extracted_tags)
        # assert
        expected_tags = [child for child in read_sample_file('sample_vacancy_extracted').children if type(child) is Tag]
        assert_that(extracted_tags, equal_to(expected_tags))

    def test_is_relevant_with_relevant_tag_returns_true(self):
        # arrange
        tag_p = create_tag('<p></p>')
        tag_div = create_tag('<div></div>')
        tag_div_nested = create_tag('<div><img /></div>')
        # act/assert
        assert_that(html_extractor.is_relevant(tag_p), is_(not_(None)))
        assert_that(html_extractor.is_relevant(tag_div), is_(not_(None)))
        assert_that(html_extractor.is_relevant(tag_div_nested), is_(not_(None)))

    def test_is_relevant_with_irrelevant_tag_returns_false(self):
        # arrange
        tag_img = create_tag('<img/>')
        tag_form = create_tag('<form></form>')
        # act/assert
        assert_that(html_extractor.is_relevant(tag_img), is_(None))
        assert_that(html_extractor.is_relevant(tag_form), is_(None))

    def test_remove_all_attributes_without_whitelist_removes_all_attributes(self):
        # arrange
        tag = create_tag('<span lang="de" xml:lang="de">Kontakt</span>')
        # act
        tag = html_extractor.remove_all_attrs(tag)
        # assert
        assert_that(str(tag), is_('<span>Kontakt</span>'))
        assert_that(tag.attrs, is_(empty()))

    def test_strip_tag_without_inner_markup_returns_only_text(self):
        # arrange
        element = create_tag('<p>\r\n       foo             \r\n</p>')
        # act
        result = html_extractor.strip_content(element)
        # assert
        assert_that(str(result), equal_to('<p>foo</p>'))

    def test_contains_children_without_children_attribute_returns_false(self):
        # arrange
        tag = object()
        # act
        result = html_extractor.contains_children(tag)
        # assert
        assert_that(result, is_(False))

    def test_contains_children_with_children_attribute_empty_list_returns_false(self):
        # arrange
        element = NavigableString('foo')
        # act
        result = html_extractor.contains_children(element)
        # assert
        assert_that(result, is_(False))

    def test_contains_children_with_children_attribute_not_empty_list_returns_false(self):
        # arrange
        element = BeautifulSoup('<div><div>foo</div></div>', 'html.parser')
        # act
        result = html_extractor.contains_children(element)
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
        result = html_extractor.is_nested(element_with_relevant_children)
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
        result = html_extractor.is_nested(element_with_relevant_children)
        # assert
        assert_that(result, is_(True))
