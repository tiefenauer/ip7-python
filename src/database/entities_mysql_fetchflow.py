import datetime

from pony.orm import Required, Database, Optional

mysqldb = Database()


# Entities for mysql@localhost:fetchflow
class Labeled_Text(mysqldb.Entity):
    title = Optional(str)
    contenttype = Optional(str)
    html = Optional(bytes, column='contentbytes')
    migrated = Required(bool)
    migrateable = Required(bool)


class Job_Titles(mysqldb.Entity):
    labeled_text_id = Required(int)
    job_title = Required(str)
    job_count = Required(int)
    last_update = Required(datetime.datetime)


mysqldb.bind('mysql', host='127.0.0.1', user='root', password='NAdu6004', database='fetchflow')
mysqldb.generate_mapping()
