import argparse
import json
import logging

from pony.orm import commit, db_session
from tqdm import tqdm

from src.database.entities_pg import X28_HTML
from src.importer.x28_json_importer import X28JsonImporter
from src.util.log_util import log_setup

log_setup()

parser = argparse.ArgumentParser(description="""
Reads X28 JSON data from a directory into a local postgres database. Only the most important attributes are read.
""")
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=False)')
args = parser.parse_args()

log_setup()
log = logging.getLogger(__name__)

if __name__ == '__main__':
    importer = X28JsonImporter()

    if args.truncate:
        importer.truncate()

    with db_session:
        for text in tqdm(importer, total=importer.num_files, unit=' files'):
            jsonobj = json.loads(text)
            language = jsonobj['language'] if 'language' in jsonobj else None
            x28_id = jsonobj['id']
            title = jsonobj['title']
            html = jsonobj['htmlcontent']
            plaintext = jsonobj['plaincontent']
            url = jsonobj['url']
            workquota_min = 0
            workquota_max = 0
            if jsonobj['workquota'] and jsonobj['workquota']['minumum']:
                workquota_min = jsonobj['workquota']['minumum']
            if jsonobj['workquota'] and jsonobj['workquota']['maximum']:
                workquota_max = jsonobj['workquota']['maximum']

            query = X28_HTML.select(lambda r: r.x28_id == x28_id)
            if query.count() > 1:
                # update existing record
                for row in query:
                    if language:
                        row.language = language
                    row.html = html
                    row.plaintext = plaintext
                    row.url = url
                    row.title = title
                    row.workquota_min = workquota_min
                    row.workquota_max = workquota_max
                    commit()
            else:
                # add new record
                X28_HTML(x28_id=x28_id,
                         language=language,
                         html=html,
                         plaintext=plaintext,
                         url=url,
                         title=title,
                         workquota_min=workquota_min,
                         workquota_max=workquota_max)
                commit()
