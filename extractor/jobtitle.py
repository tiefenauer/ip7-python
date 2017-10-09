from bs4 import BeautifulSoup

def extractJobTitle(record):
    print(record)
    html = extractHtml(record)
    print(html)

def extractHtml(record):
    return BeautifulSoup(record['contentbytes'], 'html.parser')