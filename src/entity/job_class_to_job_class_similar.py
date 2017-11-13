from pony.orm import Database

from src.entity.Entity import Entity


class JobClassToJobClassSimilar(Database.Entity):
    def insert(self, **kwargs):
        pass

    def get_table_name(self):
        return 'job_class_to_job_class_similar'
