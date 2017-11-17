from pony.orm import Required, Database

# pny.sql_debug(True)

DB_PG_FETCHFLOW = Database()


# Entities for postgres@localhost:fetchflow
class Labeled_Text_Preprocessed(DB_PG_FETCHFLOW.Entity):
    content = Required(str)
    fetchflow_id = Required(int)


DB_PG_FETCHFLOW.bind('postgres', host='127.0.0.1', user='postgres', password='postgres', database='fetchflow')
DB_PG_FETCHFLOW.generate_mapping()
