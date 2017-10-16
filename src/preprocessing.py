from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from src import html_extractor

stopwords_de = set(stopwords.words('german'))


def parse(markup):
    return BeautifulSoup(markup, 'html.parser')


def remove_html_clutter(soup):
    tags = []
    html_extractor.extract_tags(soup, tags)
    return tags


def remove_stop_words(text):
    return ' '.join([word for word in text.split(' ') if word not in stopwords_de])


def remove_stopwords(tags):
    return tags
