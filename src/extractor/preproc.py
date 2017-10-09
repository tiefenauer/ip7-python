from bs4 import BeautifulSoup
import re

# only these tags will be considered
RELEVANT_TAGS = ['p', 'h1', 'h2', 'h3', 'span', 'div', 'title', 'ul', 'ol']
# these tags will be filtered out without replacement
IRRELEVANT_TAGS = ['meta', 'link', 'style', 'script', 'noscript', 'iframe', 'form', 'input', 'img']


def extract_relevant_tags(record):
    soup = BeautifulSoup(record['contentbytes'], 'html.parser')
    extracted_tags = []
    extract_tags(soup, extracted_tags)
    return extracted_tags


def print_tags(tags):
    for tag in tags:
        print(tag)


def extract_tags(tag, tags=[]):
    if contains_relevant_children(tag):
        # nested tag
        for el in (el for el in tag.children if el.string != '\n'):
            extract_tags(el, tags)
        return

    # leaf tag
    if is_relevant(tag) and tag not in tags:
        tag = strip_tag(tag)
        if has_content(tag):
            tags.append(tag)


def is_relevant(tag, regexes=RELEVANT_TAGS):
    # make a regex that matches if any of
    combined = "(" + ")|(".join(regexes) + ")"
    return tag.name and re.match(combined, tag.name)


def contains_relevant_children(el):
    if hasattr(el, 'findAll'):
        # el is a Tag with possible nested tags
        relevant_children = el.findAll(RELEVANT_TAGS)
        return len(relevant_children) > 0
    # el is no Tag
    return contains_children(el)


def contains_children(tag):
    return hasattr(tag, 'children') and len(list(tag.children)) > 0


def contains_descendants(tag):
    return hasattr(tag, 'descendants') and len(list(tag.descendants)) > 0


def strip_tag(tag):
    # this will not work because inner markup such as <strong> would be destroyed!
    stripped = tag.getText(strip=True, separator=' ')
    if len(stripped) > 0:
        tag.string = stripped
    return tag

    #TODO: Find better version
    # stripped = re.sub('\s+', ' ', str(tag.getText()))
    #whitespaces = re.compile(r'[^a-zA-Z\d\s:]')
    #[el.text.replace('\r', ' ').replace('\n', ' ').replace(' ', '') for el in tag.findAll() if el.name != 'br']
    # for innerEl in [el for el in tag.findAll()]:
    #     if innerEl.name == 'br':
    #         innerEl.extract()
    #     else:
    #         stripped = innerEl.text.replace('\r', '').replace('\n', '').strip()
    #         innerEl.string = stripped
    # return tag


def has_content(tag):
    return len(tag.getText(strip=True)) > 0


def writeToFile(soup):
    with open(str(soup.title.getText(strip=True)) + '.html', 'w') as file:
        file.write(str(soup))
