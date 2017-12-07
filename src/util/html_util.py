from bs4 import Tag

# only these tags will be considered
RELEVANT_TAGS = {'p', 'h1', 'h2', 'h3', 'span', 'div', 'title', 'ul', 'ol', 'strong'}


def extract_tags(soup, tags=[]):
    if is_nested(soup):
        # nested tag
        for el in (el for el in soup.children if el.string != '\n'):
            extract_tags(el, tags)
        return

    # leaf tag
    if is_relevant(soup) and soup not in tags:
        soup = strip_content(soup)
        soup = remove_all_attrs(soup)
        if len(soup.getText(strip=True)) > 0:
            tags.append(soup)


def is_nested(el):
    if type(el) is Tag:
        # el is a Tag with possible nested tags
        relevant_children = el.findAll(RELEVANT_TAGS)
        return len(relevant_children) > 0
    # el is no Tag
    return contains_children(el)


def is_relevant(tag):
    return tag.name in RELEVANT_TAGS


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


def remove_tags(tags):
    return (tag.get_text() for tag in tags)
