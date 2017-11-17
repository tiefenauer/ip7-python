import datetime
from pony.orm import Required, Database

DB_MYSQL_FETCHFLOW = Database()


# Entities for mysql@localhost:fetchflow
class Labeled_Text(DB_MYSQL_FETCHFLOW.Entity):
    title = Required(str)
    html = Required(bytes, column='contentbytes')


class Job_Titles(DB_MYSQL_FETCHFLOW.Entity):
    labeled_text_id = Required(int)
    job_title = Required(str)
    job_count = Required(int)
    last_update = Required(datetime.datetime)


DB_MYSQL_FETCHFLOW.bind('mysql', host='127.0.0.1', user='root', password='NAdu6004', database='fetchflow')
DB_MYSQL_FETCHFLOW.generate_mapping()
