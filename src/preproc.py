from bs4 import BeautifulSoup
from lxml import etree
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from src.util import html_util
from src.util.html_util import remove_all_attrs, strip_content

stopwords_de = set(stopwords.words('german'))
stemmer = SnowballStemmer('german', ignore_stopwords=True)
xml_parser = etree.HTMLParser(strip_cdata=False)


def preprocess(markup):
    soup = parse(markup)
    return set(tag for tag in
               (strip_content(tag) for tag in
                (remove_all_attrs(tag) for tag in soup.findAll(html_util.RELEVANT_TAGS))
                )
               if len(tag.getText(strip=True)) > 2
               )


def parse(markup):
    # lxml parser removes the CDATA section!
    return BeautifulSoup(markup, 'lxml')


def remove_html_clutter(soup):
    tags = []
    html_util.extract_tags(soup, tags)
    return tags


def remove_stop_words(text):
    return ' '.join([word for word in text.split(' ') if word not in stopwords_de])


def stem(text):
    if isinstance(text, str):
        # got text as sentence string
        return ' '.join(word for word in _stem_iterable(text.split(' ')))
    # got text as iterable
    return _stem_iterable(text)


def _stem_iterable(words):
    try:
        return (stemmer.stem(word) for word in words)
    except TypeError:
        return ()
