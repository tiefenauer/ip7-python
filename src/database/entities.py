import datetime

from pony.orm import Required, Database

# pny.sql_debug(True)

DB_FETCHFLOW_X28 = Database('postgres', host='127.0.0.1', user='postgres', password='postgres',
                            database='fetchflow')
DB_FETCHFLOW_MYSQL = Database('mysql', host='127.0.0.1', user='root', password='NAdu6004', database='fetchflow')


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
