from bs4 import BeautifulSoup
import re

RELEVANT_TAGS = ['p', 'h1', 'h2', 'h3', 'span', 'div', 'title', 'ul', 'ol']
IRRELEVANT_TAGS = ['meta', 'link', 'style', 'script', 'noscript', 'iframe', 'form', 'input', 'img']


def extract_relevant_tags(record):
    soup = BeautifulSoup(record['contentbytes'], 'html.parser')
    # writeToFile(soup)
    extracted_tags = []
    extract_tags(soup, extracted_tags)
    return extracted_tags


def print_tags(tags):
    for tag in tags:
        print(tag)


def extract_tags(tag, tags=[]):
    if has_children(tag):
        for el in (el for el in tag.children if el.string != '\n'):
            extract_tags(el, tags)
        return

    if is_relevant(tag) and tag not in tags:
        tag = strip_tag(tag)
        if has_content(tag):
            tags.append(tag)


def move_up(tags):
    all_tags = []
    for tag in tags:
        parent = tag.parent
        all_tags.append(tag.extract())
        for irr_tag in parent.findAll(IRRELEVANT_TAGS):
            irr_tag.extract()
        all_tags.append(parent)
    return all_tags


def is_relevant(tag, regexes=RELEVANT_TAGS):
    # make a regex that matches if any of
    combined = "(" + ")|(".join(regexes) + ")"
    return tag.name and re.match(combined, tag.name)


def has_children(tag):
    if hasattr(tag, 'findAll'):
        relevant_children = tag.findAll(RELEVANT_TAGS)
        return len(relevant_children) > 0
    return hasattr(tag, 'children') \
           and len(list(tag.children)) > 0


def has_descendants(tag):
    return hasattr(tag, 'descendants') \
           and len(list(tag.descendants)) > 1


def strip_tags(tags):
    stripped_tags = []
    for tag in tags:
        stripped = tag.getText(strip=True)
        if len(stripped) > 0:
            tag.string = stripped
            stripped_tags.append(tag)
    return stripped_tags


def strip_tag(tag):
    stripped = tag.getText(strip=True)
    if len(stripped) > 0:
        tag.string = stripped
    return tag


def has_content(tag):
    return len(tag.getText(strip=True)) > 0


def writeToFile(soup):
    with open(str(soup.title.getText(strip=True)) + '.html', 'w') as file:
        file.write(str(soup))
