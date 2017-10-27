class TolerantJobTitleClassificationEvaluator(object):
    def __init__(self):
        self.total_p = 0
        self.total_n = 0
        self.performance = 0
        self.desc_pattern = "positives={}, negatives={}, performance={}"

    def evaluate(self, actual_job_title, predicted_job_title):
        if actual_job_title == predicted_job_title:
            self.total_p += 1
        else:
            self.total_n += 1
        self.performance = self.total_p / (self.total_p + self.total_n)

    def get_description(self):
        return self.desc_pattern.format(self.total_p, self.total_n, "{:1.4f}".format(self.performance))