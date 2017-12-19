import unittest

from hamcrest import assert_that, only_contains, is_, contains_inanyorder
from hamcrest.core.base_matcher import BaseMatcher

from src.util import jobtitle_util as testee


class TestJobTitleUtil(unittest.TestCase):
    def test_to_male_form_in_returns_male_form(self):
        assert_that(testee.to_male_form("Schreiner"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreinerin"), is_("Schreiner"))
        assert_that(testee.to_male_form("SchreinerIn"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner/in"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner/In"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner/innen"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner/Innen"), is_("Schreiner"))
        assert_that(testee.to_male_form('Schreiner/-in'), is_('Schreiner'))
        assert_that(testee.to_male_form('Schreiner/-In'), is_('Schreiner'))
        assert_that(testee.to_male_form("Schreiner(in)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner(In)"), is_("Schreiner"))

    def test_to_male_form_in_does_with_non_append_er_to_male_form(self):
        assert_that(testee.to_male_form('Getränketechnologin'), is_('Getränketechnolog'))

    def test_to_male_form_euse_returns_male_form(self):
        assert_that(testee.to_male_form("Coiffeur"), is_("Coiffeur"))
        assert_that(testee.to_male_form("Coiffeuse"), is_("Coiffeur"))
        assert_that(testee.to_male_form("Coiffeur/euse"), is_("Coiffeur"))
        assert_that(testee.to_male_form("Coiffeur/Euse"), is_("Coiffeur"))
        assert_that(testee.to_male_form("Coiffeur/-euse"), is_("Coiffeur"))
        assert_that(testee.to_male_form("Coiffeur/-Euse"), is_("Coiffeur"))

    def test_to_male_form_frau_returns_male_form(self):
        assert_that(testee.to_male_form("Kaufmann"), is_("Kaufmann"))
        assert_that(testee.to_male_form("Kauffrau"), is_("Kaufmann"))
        assert_that(testee.to_male_form("Kaufmann/frau"), is_("Kaufmann"))
        assert_that(testee.to_male_form("Kaufmann/Frau"), is_("Kaufmann"))
        assert_that(testee.to_male_form("Kaufmann/-frau"), is_("Kaufmann"))
        assert_that(testee.to_male_form("Kaufmann/-Frau"), is_("Kaufmann"))

    def test_to_male_form_person_returns_male_form(self):
        assert_that(testee.to_male_form('Fachperson'), is_('Fachmann'))

    def test_to_male_form_mw_returns_male_form(self):
        assert_that(testee.to_male_form("Schreiner (m/w)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner (M/W)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   (m/w)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   (M/W)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner m/w"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner M/W"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   m/w"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   M/W"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner mw"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner MW"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   mw"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   MW"), is_("Schreiner"))

    def test_to_male_form_wm_returns_male_form(self):
        assert_that(testee.to_male_form("Schreiner (w/m)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   (w/m)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner (W/M)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   (W/M)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner w/m"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   w/m"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner W/M"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   W/M"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner wm"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   wm"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner WM"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   WM"), is_("Schreiner"))

    def test_to_male_form_mf_returns_male_form(self):
        assert_that(testee.to_male_form("Schreiner (m/f)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner (M/F)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   (m/f)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   (M/F)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner m/f"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner M/F"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   m/f"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   M/F"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner mf"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner MF"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   mf"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   MF"), is_("Schreiner"))

    def test_to_male_form_fm_returns_male_form(self):
        assert_that(testee.to_male_form("Schreiner (f/m)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner (F/M)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   (f/m)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   (F/M)"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner f/m"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner F/M"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   f/m"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner   F/M"), is_("Schreiner"))
        assert_that(testee.to_male_form("Schreiner fm"), is_("Schreiner fm"))
        assert_that(testee.to_male_form("Schreiner FM"), is_("Schreiner FM"))
        assert_that(testee.to_male_form("Schreiner   fm"), is_("Schreiner   fm"))  # do NOT replace fm without slashes
        assert_that(testee.to_male_form("Schreiner   FM"), is_("Schreiner   FM"))  # do NOT replace FM without slashes

    def test_to_male_form_hyphenated_job_name_is_unchanged(self):
        assert_that(testee.to_male_form('Kupfer-Spleisser'), is_('Kupfer-Spleisser'))

    def test_to_female_form_returns_female_form(self):
        assert_that(testee.to_female_form("Schreiner"), is_("Schreinerin"))
        assert_that(testee.to_female_form("Coiffeur"), is_("Coiffeuse"))
        assert_that(testee.to_female_form("Kaufmann"), is_("Kauffrau"))

    def test_to_female_form_person_returns_female_form(self):
        assert_that(testee.to_female_form('Fachperson'), is_('Fachfrau'))

    def test_to_female_form_camel_cased_returns_female_form(self):
        assert_that(testee.to_female_form_camel_cased("Schreiner"), is_("SchreinerIn"))

    def test_to_female_form_brackets_returns_female_form(self):
        assert_that(testee.to_female_form_brackets("Schreiner"), is_("Schreiner(in)"))

    def test_to_female_form_irregular_form_returns_male_form(self):
        assert_that(testee.to_female_form('Koch'), is_('Koch'))
        assert_that(testee.to_female_form('Arzt'), is_('Arzt'))

    def test_to_female_form_camel_cased_irregular_form_returns_male_form(self):
        assert_that(testee.to_female_form_camel_cased('Koch'), is_('Koch'))
        assert_that(testee.to_female_form_camel_cased('Arzt'), is_('Arzt'))

    def test_to_female_form_brackets_form_returns_male_form(self):
        assert_that(testee.to_female_form_brackets('Koch'), is_('Koch'))
        assert_that(testee.to_female_form_brackets('Arzt'), is_('Arzt'))

    def test_to_female_form_hyphenated_job_name_is_unchanged(self):
        assert_that(testee.to_female_form('Kupfer-Spleisser'), is_('Kupfer-Spleisserin'))

    def test_to_female_form_camel_cased_hyphenated_job_name_is_unchanged(self):
        assert_that(testee.to_female_form_camel_cased('Kupfer-Spleisser'), is_('Kupfer-SpleisserIn'))

    def test_to_female_form_brackets_hyphenated_job_name_is_unchanged(self):
        assert_that(testee.to_female_form_brackets('Kupfer-Spleisser'), is_('Kupfer-Spleisser(in)'))

    def test_to_slashed_form_returns_hyphenated(self):
        assert_that(testee.to_slashed_form('Schreiner'), is_('Schreiner/in'))
        assert_that(testee.to_slashed_form('Coiffeur'), is_('Coiffeur/euse'))
        assert_that(testee.to_slashed_form('Kaufmann'), is_('Kaufmann/frau'))

    def test_to_slashed_hyphen_form_returns_slashed_hyphen(self):
        assert_that(testee.to_slashed_hyphen_form('Schreiner'), is_('Schreiner/-in'))
        assert_that(testee.to_slashed_hyphen_form('Coiffeur'), is_('Coiffeur/-euse'))
        assert_that(testee.to_slashed_hyphen_form('Kaufmann'), is_('Kaufmann/-frau'))

    def test_to_mw_form_brackets_slashed_returns_mw_form(self):
        assert_that(testee.to_mw_form_brackets_slashed('Schreinerin'), is_('Schreiner (m/w)'))
        assert_that(testee.to_mw_form_brackets_slashed('Coiffeuse'), is_('Coiffeur (m/w)'))
        assert_that(testee.to_mw_form_brackets_slashed('Kauffrau'), is_('Kaufmann (m/w)'))

    def test_to_mw_form_slashed_returns_mw_form(self):
        assert_that(testee.to_mw_form_slashed('Schreinerin'), is_('Schreiner m/w'))
        assert_that(testee.to_mw_form_slashed('Coiffeuse'), is_('Coiffeur m/w'))
        assert_that(testee.to_mw_form_slashed('Kauffrau'), is_('Kaufmann m/w'))

    def test_to_mw_form_returns_mw_form(self):
        assert_that(testee.to_mw_form('Schreinerin'), is_('Schreiner mw'))
        assert_that(testee.to_mw_form('Coiffeuse'), is_('Coiffeur mw'))
        assert_that(testee.to_mw_form('Kauffrau'), is_('Kaufmann mw'))

    def test_to_wm_form_brackets_slashed_returns_mw_form(self):
        assert_that(testee.to_wm_form_brackets_slashed('Schreinerin'), is_('Schreiner (w/m)'))
        assert_that(testee.to_wm_form_brackets_slashed('Coiffeuse'), is_('Coiffeur (w/m)'))
        assert_that(testee.to_wm_form_brackets_slashed('Kauffrau'), is_('Kaufmann (w/m)'))

    def test_to_wm_form_slashed_returns_mw_form(self):
        assert_that(testee.to_wm_form_slashed('Schreinerin'), is_('Schreiner w/m'))
        assert_that(testee.to_wm_form_slashed('Coiffeuse'), is_('Coiffeur w/m'))
        assert_that(testee.to_wm_form_slashed('Kauffrau'), is_('Kaufmann w/m'))

    def test_to_wm_form_returns_mw_form(self):
        assert_that(testee.to_wm_form('Schreinerin'), is_('Schreiner wm'))
        assert_that(testee.to_wm_form('Coiffeuse'), is_('Coiffeur wm'))
        assert_that(testee.to_wm_form('Kauffrau'), is_('Kaufmann wm'))

    def test_to_spaced_form_returns_correct_form(self):
        assert_that(testee.to_spaced_form('Elektro', 'Monteur'), is_('Elektro Monteur'))
        assert_that(testee.to_spaced_form('Elektro', 'monteur'), is_('Elektro Monteur'))
        assert_that(testee.to_spaced_form('elektro', 'Monteur'), is_('Elektro Monteur'))
        assert_that(testee.to_spaced_form('elektro', 'monteur'), is_('Elektro Monteur'))

    def test_to_hyphenated_form_returns_correct_form(self):
        assert_that(testee.to_hyphenated_form('Elektro', 'Monteur'), is_('Elektro-Monteur'))
        assert_that(testee.to_hyphenated_form('Elektro', 'monteur'), is_('Elektro-Monteur'))
        assert_that(testee.to_hyphenated_form('elektro', 'Monteur'), is_('Elektro-Monteur'))
        assert_that(testee.to_hyphenated_form('elektro', 'monteur'), is_('Elektro-Monteur'))

    def test_to_concatenated_form_returns_correct_form(self):
        assert_that(testee.to_concatenated_form('Elektro', 'Monteur'), is_('Elektromonteur'))
        assert_that(testee.to_concatenated_form('Elektro', 'monteur'), is_('Elektromonteur'))
        assert_that(testee.to_concatenated_form('elektro', 'monteur'), is_('Elektromonteur'))
        assert_that(testee.to_concatenated_form('elektro', 'Monteur'), is_('Elektromonteur'))

    def test_find_single_match(self):
        # arrange / act
        result = testee.find('Wir suchen einen 20-jährigen Schreiner mit 30 Jahren Erfahrung', 'Schreiner')
        # assert
        assert_that(result, only_contains(
            match_item_for_job_name('Schreiner')
        ))

    def test_find_suffix_in(self):
        # arrange/act
        result_m = testee.find("Wir suchen eine Schreinerin welche gerne arbeitet", 'Schreiner')
        # assert
        assert_that(result_m, only_contains(match_item_for_job_name('Schreinerin')))

    def test_find_suffix_euse(self):
        # arrange/act
        result = testee.find('Wir suchen eine Coiffeuse welche gerne arbeitet', 'Coiffeur')
        # assert
        assert_that(result, only_contains(match_item_for_job_name('Coiffeuse')))

    def test_find_suffix_frau(self):
        # arrange/act
        result = testee.find('Wir suchen eine Kauffrau welche gerne arbeitet', 'Kaufmann')
        # assert
        assert_that(result, only_contains(match_item_for_job_name('Kauffrau')))

    def test_find_slashed_in(self):
        # arrange/act
        result_hyphen = testee.find('Wir suchen eine(n) Schreiner/-in welche gerne arbeitet', 'Schreiner')
        result_no_hypen = testee.find('Wir suchen eine(n) Schreiner/in welche gerne arbeitet', 'Schreiner')
        # assert
        assert_that(result_hyphen, only_contains(match_item_for_job_name('Schreiner/-in')))
        assert_that(result_no_hypen, only_contains(match_item_for_job_name('Schreiner/in')))

    def test_find_slashed_euse(self):
        # arrange/act
        result_hyphen = testee.find('Wir suchen eine(n) Coiffeur/-euse welche gerne arbeitet', 'Coiffeur')
        result_no_hyphen = testee.find('Wir suchen eine(n) Coiffeur/euse welche gerne arbeitet', 'Coiffeur')
        # assert
        assert_that(result_hyphen, only_contains(match_item_for_job_name('Coiffeur/-euse')))
        assert_that(result_no_hyphen, only_contains(match_item_for_job_name('Coiffeur/euse')))

    def test_find_slashed_frau(self):
        # arrange/act
        result_hyphen = testee.find('Wir suchen eine(n) Kaufmann/-frau welche gerne arbeitet', 'Kaufmann')
        result_no_hypen = testee.find('Wir suchen eine(n) Kaufmann/frau welche gerne arbeitet', 'Kaufmann')
        # assert
        assert_that(result_hyphen, only_contains(match_item_for_job_name('Kaufmann/-frau')))
        assert_that(result_no_hypen, only_contains(match_item_for_job_name('Kaufmann/frau')))

    def test_find_multiple_match(self):
        # arrange/act
        result = testee.find('Wir suchen einen Schreiner oder eine Schreinerin, der bei uns arbeitet', 'Schreiner')
        # assert
        assert_that(result, only_contains(
            match_item_for_job_name('Schreiner'),
            match_item_for_job_name('Schreinerin')
        ))

    def test_create_write_variants_compound_job_name_creates_hyphenated_and_spaced_form(self):
        assert_that(testee.create_write_variants('Facharzt'), only_contains(
            'Facharzt',
            'Fach-Arzt',
            'Fach Arzt'
        ))
        assert_that(testee.create_write_variants('Servicemonteur'), only_contains(
            'Servicemonteur',
            'Service-Monteur',
            'Service Monteur'
        ))

    def test_create_write_variants_compound_spaced_job_name_creates_hyphenated_and_spaced_form(self):
        assert_that(testee.create_write_variants('Facharzt Arbeitsmedizin'), only_contains(
            'Facharzt Arbeitsmedizin',
            'Fach-Arzt Arbeitsmedizin',
            'Fach Arzt Arbeitsmedizin'
        ))

    def test_create_write_variants_hyphenated_job_name_creates_hyphenated_and_spaced_form(self):
        assert_that(testee.create_write_variants('Event-Manager'), only_contains(
            'Event-Manager',
            'Eventmanager',
            'Event Manager'
        ))

    def test_create_gender_variants_returns_gender_variants(self):
        # arrange
        job_name = 'Schreiner'
        # act
        result = testee.create_gender_variants(job_name)
        # assert
        assert_that(result, contains_inanyorder('Schreiner',
                                                'Schreinerin',
                                                'SchreinerIn',
                                                'Schreiner(in)',
                                                'Schreiner/-in',
                                                'Schreiner/in',
                                                'Schreiner (m/w)',
                                                'Schreiner m/w',
                                                'Schreiner mw',
                                                'Schreiner (w/m)',
                                                'Schreiner w/m',
                                                'Schreiner wm'
                                                )
                    )

    def test_create_gender_variants_does_not_contain_duplicates(self):
        # arrange
        job_name = "Koch"
        # act
        result = testee.create_gender_variants(job_name)
        # assert
        assert_that(result, contains_inanyorder('Koch',
                                                'Koch (m/w)',
                                                'Koch m/w',
                                                'Koch mw',
                                                'Koch (w/m)',
                                                'Koch w/m',
                                                'Koch wm'
                                                ),
                    "For job names with no easy female form do not return duplicates")

    def test_count_variant_in_returns_correct_count(self):
        # arrange
        string = """
        Polymechaniker
        Polymechanikerin
        PolymechanikerIn
        Polymechaniker/in
        Polymechaniker/In
        Polymechaniker/-in
        Polymechaniker/-In
        Polymechaniker (m/w)
        Polymechaniker   (m/w)
        Polymechaniker (mw)
        Polymechaniker   (mw)
        Polymechaniker mw
        Polymechaniker   mw
        Polymechaniker/Polymechanikerin
        """
        # act/assert
        assert_that(testee.count_variant('Polymechaniker', string), is_(2))
        assert_that(testee.count_variant('Polymechanikerin', string), is_(2))
        assert_that(testee.count_variant('PolymechanikerIn', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker/in', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker/In', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker/-in', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker/-In', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker (m/w)', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker   (m/w)', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker (mw)', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker   (mw)', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker mw', string), is_(1))
        assert_that(testee.count_variant('Polymechaniker   mw', string), is_(1))

    def test_count_variant_euse_returns_correct_count(self):
        # arrange
        string = """
        Coiffeur
        Coiffeuse
        Coiffeur/euse
        Coiffeur/-euse
        Coiffeur (m/w)
        Coiffeur   (m/w)
        Coiffeur (mw)
        Coiffeur   (mw)
        Coiffeur mw
        Coiffeur   mw
        Coiffeur/Coiffeuse
        """
        # act/assert
        assert_that(testee.count_variant('Coiffeur', string), is_(2))
        assert_that(testee.count_variant('Coiffeuse', string), is_(2))
        assert_that(testee.count_variant('Coiffeur/euse', string), is_(1))
        assert_that(testee.count_variant('Coiffeur/-euse', string), is_(1))
        assert_that(testee.count_variant('Coiffeur (m/w)', string), is_(1))
        assert_that(testee.count_variant('Coiffeur   (m/w)', string), is_(1))
        assert_that(testee.count_variant('Coiffeur (mw)', string), is_(1))
        assert_that(testee.count_variant('Coiffeur   (mw)', string), is_(1))
        assert_that(testee.count_variant('Coiffeur mw', string), is_(1))
        assert_that(testee.count_variant('Coiffeur   mw', string), is_(1))

    def test_normalize_job_name_with_empty_values_returns_input(self):
        # sanity check
        assert_that(testee.normalize_job_name(None), is_(None))
        assert_that(testee.normalize_job_name(''), is_(''))

    def test_normalize_job_name_normalizes_job_name(self):
        # male forms: -er
        assert_that(testee.normalize_job_name('Schreiner'), is_('schrein'))
        assert_that(testee.normalize_job_name('Schreinerin'), is_('schrein'))
        assert_that(testee.normalize_job_name('SchreinerIn'), is_('schrein'))
        assert_that(testee.normalize_job_name('Schreiner/in'), is_('schrein'))
        assert_that(testee.normalize_job_name('Schreiner/In'), is_('schrein'))
        assert_that(testee.normalize_job_name('Schreiner/-in'), is_('schrein'))
        assert_that(testee.normalize_job_name('Schreiner/-In'), is_('schrein'))
        assert_that(testee.normalize_job_name('Schreiner(in)'), is_('schrein'))
        assert_that(testee.normalize_job_name('Schreiner(In)'), is_('schrein'))

        # male forms: -eur
        assert_that(testee.normalize_job_name('Coiffeur'), is_('coiffeur'))
        assert_that(testee.normalize_job_name('Coiffeuse'), is_('coiffeur'))
        assert_that(testee.normalize_job_name('Coiffeur/euse'), is_('coiffeur'))
        assert_that(testee.normalize_job_name('Coiffeur/Euse'), is_('coiffeur'))
        assert_that(testee.normalize_job_name('Coiffeur/-euse'), is_('coiffeur'))
        assert_that(testee.normalize_job_name('Coiffeur/-Euse'), is_('coiffeur'))

    def test_normalize_job_title_with_empty_values_returns_original_values(self):
        assert_that(testee.normalize_job_title(None), is_(None))
        assert_that(testee.normalize_job_title(''), is_(''))

    def test_normalize_job_title_returns_lowercase(self):
        assert_that(' '.join(testee.normalize_job_title('Text')), is_('text'))

    def test_normalize_job_title_with_gender_forms_returns_stems(self):
        assert_that(' '.join(testee.normalize_job_title('Polymechaniker')), is_('polymechan'))
        assert_that(' '.join(testee.normalize_job_title('Polymechanikerin')), is_('polymechan'))
        assert_that(' '.join(testee.normalize_job_title('PolymechanikerIn')), is_('polymechan'))
        assert_that(' '.join(testee.normalize_job_title('Polymechaniker/-in')), is_('polymechan'))
        assert_that(' '.join(testee.normalize_job_title('Polymechaniker/in')), is_('polymechan'))
        assert_that(' '.join(testee.normalize_job_title('Polymechaniker/In')), is_('polymechan'))

    def test_normalize_job_title_with_neutral_or_femal_form_returns_male_forms(self):
        assert_that(' '.join(testee.normalize_job_title('Fachperson')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachfrau')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Coiffeuse')), is_('coiffeur'))

    def test_normalize_job_title_with_mw_forms_returns_male_forms(self):
        assert_that(' '.join(testee.normalize_job_title('Fachperson (m/w)')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson (M/W)')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson m/w')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson M/W')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson mw')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson MW')), is_('fachmann'))

        assert_that(' '.join(testee.normalize_job_title('Fachperson (m/f)')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson (M/F)')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson m/f')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson M/F')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson mf')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson MF')), is_('fachmann'))

    def test_normalize_job_title_with_wm_forms_returns_male_forms(self):
        assert_that(' '.join(testee.normalize_job_title('Fachperson (w/m)')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson (W/M)')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson w/m')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson W/M')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson wm')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson WM')), is_('fachmann'))

        assert_that(' '.join(testee.normalize_job_title('Fachperson (f/m)')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson (F/M)')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson f/m')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson F/M')), is_('fachmann'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson fm')), is_('fachmann fm'))
        assert_that(' '.join(testee.normalize_job_title('Fachperson FM')), is_('fachmann fm'))

    def test_normalize_job_title_with_percentage_removes_percentage(self):
        assert_that(' '.join(testee.normalize_job_title('Schreiner 100%')), is_('schrein'))
        assert_that(' '.join(testee.normalize_job_title('Schreiner 80%')), is_('schrein'))

    def test_normalize_job_title_with_percentage_range_removes_percentage_range(self):
        assert_that(' '.join(testee.normalize_job_title('Schreiner 80-100%')), is_('schrein'))
        assert_that(' '.join(testee.normalize_job_title('Schreiner 70-80%')), is_('schrein'))
        assert_that(' '.join(testee.normalize_job_title('Junior Accountant (m/w) 80 - 100%')), is_('junior accountant'))

    def test_normalize_job_title_with_slashed_expression_returns_single_words(self):
        assert_that(' '.join(testee.normalize_job_title('Tagesmutter/Tagesfamilie')), is_('tagesmutt tagesfamili'))
        assert_that(' '.join(testee.normalize_job_title('Schulbusfahrerin/-fahrer')), is_('schulbusfahrerin fahr'))

    def test_normalize_job_title_with_hyphenated_expression_returns_single_words(self):
        assert_that(' '.join(testee.normalize_job_title('LWL-Spleisser')), is_('lwl spleiss'))

    def test_normalize_job_title_normalizes_text(self):
        # arrange
        text = 'Text, Fachperson und Arzt oder Schreinerin Polymechaniker/in (m/w)'
        # act
        result = testee.normalize_job_title(text)
        result_text = ' '.join(item for item in result)
        # assert
        assert_that(result_text, is_('text fachmann arzt schrein polymechan'))


def match_item_for_job_name(job_name):
    return IsMatchItemForJobName(job_name)


class IsMatchItemForJobName(BaseMatcher):
    def __init__(self, job_name):
        self.job_name = job_name

    def _matches(self, item):
        return item.group() == self.job_name

    def describe_to(self, description):
        description.append_text('match item with group matching \'') \
            .append_text(self.job_name) \
            .append_text('\'')
