import logging
import os
import pickle

import nltk

from src.classifier.classifier_based_german_tagger import ClassifierBasedGermanTagger
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

data_dir = 'D:/code/ip7-python/resource/models/nltk'
corpus_name = 'tiger_release_aug07.corrected.16012013.conll09'
tagger_pickle = 'nltk_german_classifier_data.pickle'
corpus_path = os.path.join(data_dir, corpus_name)
german_pos_tagger_path = os.path.join(data_dir, tagger_pickle)

if __name__ == '__main__':
    log.info('reading corpus...')
    corp = nltk.corpus.ConllCorpusReader('.', corpus_name,
                                         ['ignore', 'words', 'ignore', 'ignore', 'pos'],
                                         encoding='utf-8')

    tagged_sents = corp.tagged_sents()
    log.info('got {} tagged sents'.format(len(tagged_sents)))
    # random.shuffle(tagged_sents)

    split_perc = 0.1
    split_size = int(len(tagged_sents) * split_perc)
    train_sents, test_sents = tagged_sents[split_size:], tagged_sents[:split_size]

    log.info('training german tagger with {} tagged sentences...'.format(len(train_sents)))
    tagger = ClassifierBasedGermanTagger(train=train_sents)
    log.info('evaluating accuracy with {} tagged sentences...'.format(len(test_sents)))
    accuracy = tagger.evaluate(test_sents)
    log.info('accuracy is: {}'.format(accuracy))
    log.info('training again with whole data...')
    tagger = ClassifierBasedGermanTagger(train=tagged_sents)
    sample = 'Das ist ein einfacher Test'
    log.info('Checking tagging functionality with sample sentence: ' + sample)
    tags = tagger.tag(sample.split(' '))
    print(tags)
    log.info('pickling tagger')
    with open(german_pos_tagger_path, 'wb') as f:
        pickle.dump(tagger, f)
    log.info('done! Have a nice day')
