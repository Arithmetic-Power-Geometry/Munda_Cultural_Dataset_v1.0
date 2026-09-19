from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'data' / 'source_census' / 'rau_2019_csv_manifestation_access_run181_2026-09-11.json'
LOG = ROOT / 'data' / 'source_census' / 'search_log_run181.jsonl'
MMSC = ROOT / 'data' / 'source_census' / 'mmsc_index.json'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def test_run181_rau_manifestation_is_exact_but_hash_not_overclaimed():
    audit = load(AUDIT)
    assert audit['run'] == 181
    assert audit['branch'] == 'mlhkp-v2'
    assert audit['source']['doi'] == '10.5281/zenodo.3380874'
    m = audit['exact_manifestation']
    assert m['filename'] == 'pMunda_cognate_set_2019-08-29.csv'
    assert m['repository_reported_md5'] == '07e1d945a0fc6cafc4fc7afd3f1ff144'
    assert m['download_endpoint_resolved_to_text_manifestation'] is True
    assert m['manifestation_header_verified'] is True
    assert m['mundari_columns_present'] == ['mu_form', 'mu_source']
    assert m['independent_hash_recomputed'] is False
    assert m['local_byte_copy_retained_by_mlhkp'] is False


def test_run181_rights_and_cultural_boundaries_remain_closed():
    audit = load(AUDIT)
    r = audit['rights_and_cultural_access']
    e = audit['evidence_boundary']
    assert r['exact_license_value_exposed_in_retrieved_authoritative_record'] is False
    assert r['reuse_permission_inferred'] is False
    assert r['row_level_reuse_permitted_by_this_audit'] is False
    assert r['participant_consent_inferred'] is False
    assert r['community_validation_inferred'] is False
    assert r['cultural_access_inferred'] is False
    assert e['dataset_rows_ingested'] is False
    assert e['lexical_or_reconstruction_claim_promoted'] is False
    assert e['cultural_claim_promoted'] is False
    assert e['evidence_graph_count_changed'] is False
    assert audit['deduplication']['new_permanent_identity_assigned'] is False
    assert audit['deduplication']['counts_changed'] is False


def test_run181_search_log_covers_all_requested_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding='utf-8').splitlines() if line.strip()]
    classes = {row.get('class') for row in rows if row.get('class')}
    required = {
        'books_dictionaries_grammars', 'peer_reviewed_articles', 'theses_dissertations',
        'government_tri_census_lsi', 'archives', 'newspapers_periodicals', 'web_resources',
        'datasets', 'audio', 'video', 'maps', 'relevant_media'
    }
    assert required <= classes
    assert all(row['search_id'] == 'MMSC-SEARCH-000181' for row in rows)


def test_run181_remains_count_stable_until_atomic_registration():
    mmsc = load(MMSC)['metrics']
    assert mmsc['sources_discovered'] == 42
    assert mmsc['standalone_mmsc_discoveries'] == 16
    assert mmsc['web_discovery_records_observed'] == 90
    assert mmsc['web_discovery_unique_leads'] == 87
    assert mmsc['web_discovery_duplicate_records'] == 3
    assert mmsc['web_discovery_leads_counted_in_audited_identity_total'] == 14
    assert mmsc['web_discovery_unique_leads_remaining_outside_audited_identity_total'] == 73
