def doesnt_match(words):
    print('Doesn\'t match: ' + words)
    result = model_x28.doesnt_match(words.split())
    print(result)


def most_similar(word):
    if word not in x28_index2word:
        return
    print('Most similar: ' + word)
    row_format = "{:>30} {}"
    for result, score in model_x28.wv.most_similar(word):
        print(row_format.format(result, score))


def update_most_similar_job_classes():
    log.info('update_most_similar_job_classes: Updating DB with most similar jobs for trained jobs...')
    with db_session:
        # truncate previous mappings
        Job_Class_To_Job_Class_Similar.select().delete(bulk=True)
        Job_Class_Similar.select().delete(bulk=True)
        commit()
        # add new mappings
        known_and_trained_jobs = list(job_class for job_class in Job_Class.select()
                                      if job_class.job_name in model_x28.index2word)

        for job_class in tqdm(known_and_trained_jobs, unit=' rows'):
            for similar_name, score in model_x28.most_similar(job_class.job_name):
                if Job_Class_Similar.exists(job_name_similar=similar_name):
                    job_class_similar = Job_Class_Similar.get(job_name_similar=similar_name)
                else:
                    job_class_similar = Job_Class_Similar(job_name_similar=similar_name)
                commit()
                Job_Class_To_Job_Class_Similar(fk_job_class=job_class.id, fk_job_class_similar=job_class_similar.id,
                                               score=score)
    log.info('update_most_similar_job_classes: done!')