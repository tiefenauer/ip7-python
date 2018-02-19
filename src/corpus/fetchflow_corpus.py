import os

from src.util.globals import CORPUS_DIR

corpus_file = os.path.join(CORPUS_DIR, '/fetchflow.corpus')


class FetchflowCorpus(object):
    """Iterator class for corpus of Fetchflow-Vacancies. The corpus contains a list of sentences of vacancies
    whereas each sentence is read from a pre-processed corpus file
    """

    def __iter__(self):
        with open(corpus_file, encoding='utf-8') as corpus:
            for line in corpus:
                yield line
