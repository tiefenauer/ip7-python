import pony.orm as pny
from pony.orm import Required, Optional

#pny.sql_debug(True)
db = pny.Database('postgres', user='postgres', password='postgres', host='127.0.0.1', database='x28')


class Job_Class(db.Entity):
    _table = 'job_class'
    job_name = Required(str)
    job_name_stem = Optional(str)


class Job_Class_To_Job_Class_Similar(db.Entity):
    _table = 'job_class_to_job_class_similar'
    fk_job_class = Required(int)
    fk_job_class_similar = Required(int)
    score = Required(float)


class Job_Class_Similar(db.Entity):
    _table = 'job_class_similar'
    job_name_similar = Required(str)


db.generate_mapping()