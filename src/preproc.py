from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from src import html_extractor

stopwords_de = set(stopwords.words('german'))
stemmer = SnowballStemmer('german', ignore_stopwords=True)


def preprocess(markup):
    soup = parse(markup)
    return ' '.join(tag.getText() for tag in remove_html_clutter(soup))


def parse(markup):
    return BeautifulSoup(markup, 'html.parser')


def remove_html_clutter(soup):
    tags = []
    html_extractor.extract_tags(soup, tags)
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
