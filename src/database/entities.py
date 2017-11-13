import datetime

from pony.orm import Required, Optional, Database, Set

# pny.sql_debug(True)

DB_X28 = Database()
DB_FETCHFLOW_X28 = Database('postgres', host='127.0.0.1', user='postgres', password='postgres',
                            database='fetchflow')
DB_FETCHFLOW_MYSQL = Database('mysql', host='127.0.0.1', user='root', password='NAdu6004', database='fetchflow')


# Entities for postcres@localhost:x28
class Data_Train(DB_X28.Entity):
    html = Required(str)
    plaintext = Required(str)
    url = Required(str)
    title = Required(str)
    x28_id = Required(int)
    cls_fts = Set('Classification_Results')


class Job_Class(DB_X28.Entity):
    _table = 'job_class'
    job_name = Required(str)
    job_name_stem = Optional(str)
    variants = Set('Job_Class_Variant')
    similar = Set('Job_Class_To_Job_Class_Similar')


class Job_Class_Variant(DB_X28.Entity):
    job_class = Required(Job_Class, column='job_class_id')
    job_name_variant = Required(str)


class Job_Class_Similar(DB_X28.Entity):
    _table = 'job_class_similar'
    job_name_similar = Required(str)
    similar = Set('Job_Class_To_Job_Class_Similar')


class Job_Class_To_Job_Class_Similar(DB_X28.Entity):
    _table = 'job_class_to_job_class_similar'
    fk_job_class = Required(Job_Class)
    fk_job_class_similar = Required(Job_Class_Similar)
    score = Required(float)


class Classification_Results(DB_X28.Entity):
    job_class = Required(Data_Train, column='job_id')
    clf_method = Required(str)
    job_name = Required(str)
    score_strict = Required(float)
    score_tolerant = Required(float)
    score_linear = Required(float)


DB_X28.bind('postgres', host='127.0.0.1', user='postgres', password='postgres', database='x28')
DB_X28.generate_mapping()


# Entities for postgres@localhost:fetchflow
class Labeled_Text_Preprocessed(DB_FETCHFLOW_X28.Entity):
    content = Required(str)
    fetchflow_id = Required(int)


DB_FETCHFLOW_X28.generate_mapping()


# Entities for mysql@localhost:fetchflow
class Labeled_Text(DB_FETCHFLOW_MYSQL.Entity):
    title = Required(str)
    contentbytes = Required(str)


class Job_Titles(DB_FETCHFLOW_MYSQL.Entity):
    labeled_text_id = Required(int)
    job_title = Required(str)
    job_count = Required(int)
    last_update = Required(datetime.datetime)
