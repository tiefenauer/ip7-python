from pony.orm import db_session

from src.classifier.jobtitle.jobtitle_classifier_fts import FeatureBasedJobtitleFtsClassifier
from src.classifier.loe.loe_classifier import LoeClassifier
from src.database.entities_pg import Fetchflow_HTML
from src.preprocessing.loe_preprocessor import LoePreprocessor
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor

# hier gewünschte IDs einschränken (oder leere Liste für alle Rows)
my_ids = [1, 2, 3, 42]
with db_session:
    my_vacancies = Fetchflow_HTML.select(lambda row: not my_ids or row.id in my_ids)


def make_jobtitle_predictions():
    """Extrahiert den Jobtitel aus Fetchflow-Vakanzen"""

    # Preprocessor nimmt ein DOM und extrahiert aus einem DOM die relevanten Tags
    preprocessor = RelevantTagsPreprocessor()
    # Classifier nimmt eine Liste relevanter Tags und extrahiert den Jobtitel
    classifier = FeatureBasedJobtitleFtsClassifier()

    for row in my_vacancies[:100]:
        relevant_tags = preprocessor.preprocess_single(row)
        predicted_class = classifier.predict_class(relevant_tags)

        # folgenden Output aus Konsole in CSV kopieren
        print('{}\t{}\t{}'.format(row.id, row.fetchflow_id, predicted_class))


def make_loe_predictions():
    # Preprocessor nimmt ein DOM und extrahiert aus einem DOM die relevanten Tags
    preprocessor = LoePreprocessor()
    # Classifier nimmt eine Liste relevanter Tags und extrahiert den Beschäftigungsgrad
    classifier = LoeClassifier()

    for row in my_vacancies[:100]:
        relevant_tags = preprocessor.preprocess_single(row)
        workquota_min, workquota_max = classifier.predict_class(relevant_tags)
        # folgenden Output aus Konsole in CSV kopieren
        print('{}\t{}\t{}\t{}'.format(row.id, row.fetchflow_id, workquota_min, workquota_max))

