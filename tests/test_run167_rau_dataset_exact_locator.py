from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'data' / 'source_census' / 'felix_rau_2019_munda_cognate_dataset_exact_locator_run167_2026-09-10.json'
LOG = ROOT / 'data' / 'source_census' / 'search_log_run167.jsonl'
MMSC = ROOT / 'data' / 'source_census' / 'mmsc_index.json'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def test_run167_rau_exact_identity_and_manifestation():
    audit = load(AUDIT)
    assert audit['run'] == 167
    assert audit['branch'] == 'mlhkp-v2'
    assert audit['source']['doi'] == '10.5281/zenodo.3380874'
    assert audit['source']['version'] == '0.1.0'
    assert audit['source']['creator'] == 'Felix Rau'
    assert audit['source_reported_scope']['cognate_sets'] == 127
    assert 'Mundari' in audit['source_reported_scope']['languages_named_by_repository']
    assert audit['exact_manifestation']['filename'] == 'pMunda_cognate_set_2019-08-29.csv'
    assert audit['exact_manifestation']['repository_reported_md5'] == '07e1d945a0fc6cafc4fc7afd3f1ff144'
    assert audit['exact_manifestation']['independent_hash_recomputed'] is False
    assert audit['exact_manifestation']['file_bytes_acquired_by_mlhkp'] is False


def test_run167_rights_and_evidence_boundaries_are_conservative():
    audit = load(AUDIT)
    rights = audit['rights_and_cultural_access']
    boundary = audit['evidence_boundary']
    assert rights['license_text_resolved_from_rendered_record'] is False
    assert rights['reuse_permission_inferred'] is False
    assert rights['underlying_dictionary_or_pinnow_rights_inferred'] is False
    assert rights['community_validation_inferred'] is False
    assert rights['cultural_access_inferred'] is False
    assert boundary['cultural_claim_promoted'] is False
    assert boundary['lexical_or_reconstruction_claim_promoted'] is False
    assert boundary['dataset_rows_ingested'] is False
    assert boundary['evidence_graph_count_changed'] is False
    assert audit['deduplication']['new_permanent_identity_assigned'] is False
    assert audit['deduplication']['counts_changed'] is False


def test_run167_search_log_covers_all_requested_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding='utf-8').splitlines() if line.strip()]
    classes = {row.get('class') for row in rows if row.get('class')}
    required = {
        'books_dictionaries_grammars', 'peer_reviewed_articles', 'theses_dissertations',
        'government_tri_census_lsi', 'archives', 'newspapers_periodicals', 'web_resources',
        'datasets', 'audio', 'video', 'maps', 'relevant_media'
    }
    assert required <= classes
    assert all(row['search_id'] == 'MMSC-SEARCH-000167' for row in rows)


def test_run167_is_count_stable_until_full_reconciliation():
    mmsc = load(MMSC)['metrics']
    assert mmsc['sources_discovered'] == 41
    assert mmsc['standalone_mmsc_discoveries'] == 15
    assert mmsc['web_discovery_records_observed'] == 90
    assert mmsc['web_discovery_unique_leads'] == 87
    assert mmsc['web_discovery_duplicate_records'] == 3
    assert mmsc['web_discovery_leads_counted_in_audited_identity_total'] == 13
    assert mmsc['web_discovery_unique_leads_remaining_outside_audited_identity_total'] == 74
