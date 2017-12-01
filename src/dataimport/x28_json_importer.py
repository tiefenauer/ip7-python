import logging
import os

from src.database.entities_pg import X28_HTML
from src.dataimport.importer import Importer

log = logging.getLogger(__name__)


class X28JsonImporter(Importer):
    def __init__(self, dirname='D:/db/x28'):
        super(X28JsonImporter, self).__init__(X28_HTML)
        self.dirname = dirname
        self.num_files = len([name for name in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, name))])

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, fname), encoding='utf-8') as file:
                yield file.read()