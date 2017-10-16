import re

# only these tags will be considered
from copy import copy

from bs4 import Tag

RELEVANT_TAGS = {'p', 'h1', 'h2', 'h3', 'span', 'div', 'title', 'ul', 'ol'}
# these tags will be filtered out without replacement
IRRELEVANT_TAGS = {'meta', 'link', 'style', 'script', 'noscript', 'iframe', 'form', 'input', 'img'}


def extract_tags(tag, tags=[]):
    if is_nested(tag):
        # nested tag
        for el in (el for el in tag.children if el.string != '\n'):
            extract_tags(el, tags)
        return

    # leaf tag
    if is_relevant(tag) and tag not in tags:
        tag = strip_content(tag)
        tag = remove_all_attrs(tag)
        if len(tag.getText(strip=True)) > 0:
            tags.append(tag)


def is_nested(el):
    if type(el) is Tag:
        # el is a Tag with possible nested tags
        relevant_children = el.findAll(RELEVANT_TAGS)
        return len(relevant_children) > 0
    # el is no Tag
    return contains_children(el)


def is_relevant(tag, relevant_rags=RELEVANT_TAGS):
    # make a regex that matches if any of the relevant tags
    combined = "(" + ")|(".join(relevant_rags) + ")"
    return tag.name and re.match(combined, tag.name)


def strip_content(tag):
    # TODO: this does not work correctly yet because will not work because inner markup such as <strong> will be destroyed!
    stripped = tag.getText(strip=True, separator=' ')
    if len(stripped) > 0:
        tag.string = stripped
    return tag


def contains_children(tag):
    return hasattr(tag, 'children') and len(list(tag.children)) > 0


# remove all attributes
def remove_all_attrs(soup):
    for tag in soup.find_all(True):
        tag.attrs = {}
    soup.attrs = {}
    return soup


# remove all attributes except some tags
def remove_all_attrs_except(soup):
    whitelist = ['a', 'img']
    for tag in soup.find_all(True):
        if tag.name not in whitelist:
            tag.attrs = {}
    return soup


# remove all attributes except some tags(only saving ['href','src'] attr)
def remove_all_attrs_except_saving(soup):
    whitelist = ['a', 'img']
    for tag in soup.find_all(True):
        if tag.name not in whitelist:
            tag.attrs = {}
        else:
            attrs = dict(tag.attrs)
            for attr in attrs:
                if attr not in ['src', 'href']:
                    del tag.attrs[attr]
    return soup
