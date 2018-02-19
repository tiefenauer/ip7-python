# path to project root
import os

BASE_DIR = 'D:/code/ip7-python/'
# path to db root
DB_DIR = 'D:/db/'

RESOURCE_DIR = os.path.join(BASE_DIR, 'resource/')
MODELS_DIR = os.path.join(RESOURCE_DIR, 'models/')
CORPUS_DIR = os.path.join(RESOURCE_DIR, 'corpus/')

TEST_RESOURCE_DIR = os.path.join(BASE_DIR, 'test/resources/')

X28_DB_DIR = os.path.join(DB_DIR, 'x28/')

WEIGHTED_HTML_TAGS = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'strong', 'default']
