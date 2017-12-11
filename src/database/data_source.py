from abc import ABC, abstractmethod

from pony.orm import db_session


class DataSource(ABC):
    @db_session
    def __init__(self, args, entity):
        self.Entity = entity
        # calculate total number of available rows
        self.id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        num_total = self.Entity.select(lambda d: self.id < 0 or d.id == self.id).count()
        self.num_total = num_total
        # calculate effective number of rows with limit and offset
        split = args.split if hasattr(args, 'split') and args.split else 1
        self.split = int(split * self.num_total)
        self.num_rows = self.calc_num_rows(num_total, split)

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def calc_num_rows(self, num_total, split):
        """calculate number of rows to process with current splitting"""
