from pony.orm import Required, Set, Optional, Discriminator, Database

pgdb = Database()


class Fetchflow_HTML(pgdb.Entity):
    html = Required(str)
    fetchflow_id = Required(int)


class Data_Train(pgdb.Entity):
    html = Optional(str)
    plaintext = Optional(str)
    url = Optional(str)
    title = Optional(str)
    x28_id = Required(int)
    cls_fts = Set('Classification_Results')


class Job_Class(pgdb.Entity):
    _table = 'job_class'
    job_name = Required(str)
    job_name_stem = Optional(str)
    variants = Set('Job_Class_Variant')
    similar = Set('Job_Class_To_Job_Class_Similar')


class Job_Class_Variant(pgdb.Entity):
    job_class = Required(Job_Class, column='job_class_id')
    job_name_variant = Required(str)


class Job_Class_Similar(pgdb.Entity):
    _table = 'job_class_similar'
    job_name_similar = Required(str)
    similar = Set('Job_Class_To_Job_Class_Similar')


class Job_Class_To_Job_Class_Similar(pgdb.Entity):
    _table = 'job_class_to_job_class_similar'
    job_class = Required(Job_Class, column='fk_job_class')
    job_class_similar = Required(Job_Class_Similar, column='fk_job_class_similar')
    score = Required(float)


class Classification_Results(pgdb.Entity):
    clf_method = Discriminator(str)
    job_class = Required(Data_Train, column='job_id')
    job_name = Required(str)
    score_strict = Required(float)
    score_tolerant = Required(float)
    score_linear = Required(float)


class Fts_Classification_Results(Classification_Results):
    _discriminator_ = 'fts'


class Semantic_Avg_Classification_Results(Classification_Results):
    _discriminator_ = 'semantic_avg'


pgdb.bind('postgres', host='127.0.0.1', user='postgres', password='postgres', database='x28')
pgdb.generate_mapping()
