import os

import pandas
from pony.orm import db_session

from src.classifier.jobtitle.jobtitle_classifier_fts import FeatureBasedJobtitleFtsClassifier
from src.classifier.loe.loe_classifier import LoeClassifier
from src.database.entities_pg import Fetchflow_HTML
from src.preprocessing.loe_preprocessor import LoePreprocessor
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor
from src.scoring.jobtitle_scorer_linear import LinearJobtitleScorer
from src.scoring.jobtitle_scorer_strict import StrictJobtitleScorer
from src.scoring.jobtitle_scorer_tolerant import TolerantJobtitleScorer
from src.scoring.loe_scorer_linear import LinearLoeScorer
from src.scoring.loe_scorer_strict import StrictLoeScorer
from src.scoring.loe_scorer_tolerant import TolerantLoeScorer

from src.util.globals import RESOURCE_DIR

# Pfad zum File, wo die Predictions und Labels sind
evaluation_file = os.path.join(RESOURCE_DIR, 'fetchflow_evaluation.xlsx')

# hier gewünschte IDs einschränken (oder leere Liste für alle Rows)
my_ids = [1, 2, 3, 42]
with db_session:
    my_vacancies = Fetchflow_HTML.select(lambda row: not my_ids or row.id in my_ids)


def make_jobtitle_predictions():
    """Extrahiert den Jobtitel mittels Volltextsuche(Ansatz 1) aus Fetchflow-Vakanzen"""

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
    """Extrahiert den Beschäftigungsgrad aus Fetchflow-Vakanzen"""
    # Preprocessor nimmt ein DOM und extrahiert aus einem DOM die relevanten Tags
    preprocessor = LoePreprocessor()
    # Classifier nimmt eine Liste relevanter Tags und extrahiert den Beschäftigungsgrad
    classifier = LoeClassifier()

    for row in my_vacancies[:100]:
        relevant_tags = preprocessor.preprocess_single(row)
        workquota_min, workquota_max = classifier.predict_class(relevant_tags)

        # folgenden Output aus Konsole in CSV kopieren
        print('{}\t{}\t{}\t{}'.format(row.id, row.fetchflow_id, workquota_min, workquota_max))


def evaluate_predictions():
    jt_scorer_strict = StrictJobtitleScorer()
    jt_scorer_linear = LinearJobtitleScorer()
    jt_scorer_tolerant = TolerantJobtitleScorer()
    loe_scorer_strict = StrictLoeScorer()
    loe_scorer_linear = LinearLoeScorer()
    loe_scorer_tolerant = TolerantLoeScorer()

    df = pandas.read_excel(evaluation_file, header=0, index_col=0)
    for index, row in df.iterrows():
        jt_actual = row['jobtitle_actual']
        jt_prediction = row['jobtitle_predicted']

        jt_score_strict = jt_scorer_strict.calculate_score(jt_actual, jt_prediction)
        jt_score_linear = jt_scorer_linear.calculate_score(jt_actual, jt_prediction)
        jt_score_tolerant = jt_scorer_tolerant.calculate_score(jt_actual, jt_prediction)

        row['score_strict'] = jt_score_strict
        row['score_linear'] = jt_score_linear
        row['score_tolerant'] = jt_score_tolerant

        loe_actual = (row['loe_min_actual'], row['loe_max_actual'])
        loe_prediction = (row['loe_min_predicted'], row['loe_max_predicted'])

        loe_score_strict = loe_scorer_strict.calculate_score(loe_actual, loe_prediction)
        loe_score_linear = loe_scorer_linear.calculate_score(loe_actual, loe_prediction)
        loe_score_tolerant = loe_scorer_tolerant.calculate_score(loe_actual, loe_prediction)

        print('{}\t{}\t{}\t\t{}\t{}\t{}\t'.format(jt_score_strict, jt_score_linear, jt_score_tolerant, loe_score_strict,
                                                  loe_score_linear, loe_score_tolerant))


if __name__ == '__main__':
    # Schritt 3a: je nach Bedarf einen der folgenden Zeilen einkommentieren, um Predictions in der Konsole zu erhalten
    # make_jobtitel_predictions()
    # make_loe_predictions()

    # Schritt 3b: nachdem die predictions gemacht wurden diese in ein CSV kopieren und CSV in XLSX umwandeln

    # Schritt 4: Spalten umbenennen
    # Schritt 5: "echte" Labels manuell extrahieren
    # Schritt 6: "echte" Labels im Excel nachtragen

    # Schritt 7: Scores berechnen:
    evaluate_predictions()