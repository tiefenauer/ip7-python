from . import preproc

def extractJobTitle(record):
    print('Extracting job title for vacancy:', record['url'])
    tags = preproc.extract_tags(record)
    preproc.print_tags(tags)
