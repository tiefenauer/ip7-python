import logging
from abc import ABC, abstractmethod

from pony.orm import db_session, commit

log = logging.getLogger(__name__)


class Importer(ABC):

    def __init__(self, TargetEntity):
        self.TargetEntity = TargetEntity

    @db_session
    def truncate(self):
        log.info('Truncating target tables...')
        self.TargetEntity.select().delete(bulk=True)
        commit()
        log.info('...done!')

    @abstractmethod
    def __iter__(self):
        """iterate over items to be imported"""
        return