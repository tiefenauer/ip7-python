from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from src.html_extractor import extract_tags

stopwords_de = set(stopwords.words('german'))


def remove_stop_words(text):
    return ' '.join([word for word in text.split(' ') if word not in stopwords_de])


def remove_html_clutter(markup):
    soup = BeautifulSoup(markup, 'html.parser')
    tags = []
    extract_tags(soup)
    return tags
