from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def test_run165_grambank_exact_valueset_and_rights_boundary():
    a = load('data/source_census/grambank_gb317_mundari_exact_locator_run165_2026-09-10.json')
    assert a['run'] == 165
    assert a['branch'] == 'mlhkp-v2'
    assert a['source']['glottocode'] == 'mund1320'
    assert a['source']['database_license'] == 'Creative Commons Attribution 4.0 International'
    assert a['exact_datapoint']['locator'].endswith('/valuesets/GB317-mund1320')
    assert a['exact_datapoint']['feature_id'] == 'GB317'
    assert a['exact_datapoint']['coding'] == 'absent'
    assert a['exact_datapoint']['source_locator_reported_by_grambank'] == 'Osada 2008: 107-108'
    assert a['verification_state']['underlying_osada_pages_directly_inspected'] is False
    assert a['verification_state']['new_permanent_source_identity_assigned'] is False
    assert a['rights_access_consent_cultural_uncertainty']['underlying_grammar_rights_transferred_by_database_license'] is False
    assert a['rights_access_consent_cultural_uncertainty']['community_validation_inferred'] is False


def test_run165_muntts_karya_discrepancy_is_explicit_not_normalized():
    a = load('data/source_census/muntts_karya_count_manifestation_audit_run165_2026-09-10.json')
    assert a['paper_manifestation']['reported_audio_recordings'] == 26868
    assert a['karya_repository_manifestation']['reported_audio_recordings'] == 26870
    assert a['karya_repository_manifestation']['reported_female_recordings'] + a['karya_repository_manifestation']['reported_male_recordings'] == 26870
    assert a['discrepancy']['absolute_difference'] == 2
    assert a['discrepancy']['status'] == 'documented_unreconciled_manifestation_or_version_difference'
    assert a['karya_repository_manifestation']['repository_provided_sha1'] == '46c8bfceb5cf25decc8523479378793537f2bad7'
    assert a['karya_repository_manifestation']['sha1_independently_recomputed'] is False
    assert a['rights_access_consent_cultural_uncertainty']['audio_or_transcript_ingested'] is False
    assert a['rights_access_consent_cultural_uncertainty']['speaker_secondary_use_consent_verified'] is False
    assert a['counts_changed'] is False


def test_run165_search_log_covers_requested_classes_and_counts_stay_stable():
    lines = [json.loads(x) for x in (ROOT / 'data/source_census/search_log_run165.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    assert all(x['search_id'] == 'MMSC-SEARCH-000165' for x in lines)
    classes = {x.get('class') for x in lines}
    required = {'books_dictionaries_grammars','peer_reviewed_articles','theses_dissertations','government_tri_census_lsi','archives','newspapers_periodicals','web_resources','datasets','audio','video','maps','relevant_media'}
    assert required <= classes
    mmsc = load('data/source_census/mmsc_index.json')['metrics']
    assert mmsc['sources_discovered'] == 41
    assert mmsc['standalone_mmsc_discoveries'] == 15
    assert mmsc['web_discovery_records_observed'] == 90
    assert mmsc['web_discovery_unique_leads'] == 87
    assert mmsc['web_discovery_duplicate_records'] == 3
    assert mmsc['web_discovery_leads_counted_in_audited_identity_total'] == 13
    assert mmsc['web_discovery_unique_leads_remaining_outside_audited_identity_total'] == 74
