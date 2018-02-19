class X28Corpus(object):

    def __init__(self):
        self.plaintexts = []
        self.titles = []
        self.nouns = []
        self.verbs = []
        self.labels = []
        self.labels_simplified = []

    def add_sample(self, plaintext, title, nouns, verbs, label, label_simplified):
        self.plaintexts.append(plaintext)
        self.titles.append(title)
        self.nouns.append(nouns)
        self.verbs.append(verbs)
        self.labels.append(label)
        self.labels_simplified.append(label_simplified)
