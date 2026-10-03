import json
from pathlib import Path


def test_run234_ciil_manifestations_and_rights_boundary():
    p = Path('data/source_census/ciil_sanchika_additional_mundari_resources_run234_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 234
    assert data['branch'] == 'mlhkp-v2'
    ids = {s['repository_identifier'] for s in data['sources']}
    assert ids == {'BVP04859', 'BVP06110', 'BVP00242'}
    assert all(s['metadata_manifestation_verified'] is True for s in data['sources'])
    assert all(s['byte_preserving_download_acquired'] is False for s in data['sources'])
    assert all(s['independent_hash_computed'] is False for s in data['sources'])
    assert all(s['claim_level_locator_promoted'] is False for s in data['sources'])
    rights = data['rights_and_governance']
    assert rights['public_availability_treated_as_permission'] is False
    assert rights['unrestricted_redistribution_permission_inferred'] is False
    assert rights['participant_consent_inferred'] is False
    assert rights['community_validation_inferred'] is False
    assert rights['cultural_access_permission_inferred'] is False
    promotion = data['promotion']
    assert promotion['promoted_beyond_discovery_only'] is True
    assert promotion['promoted_to_claim_evidence_graph'] is False
    assert promotion['lexical_rows_ingested'] == 0
    assert data['deduplication']['new_identity_count_increment_permitted'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'


def test_run234_all_class_log_counts_and_census_boundary():
    p = Path('data/source_census/search_log_run234.jsonl')
    row = json.loads(p.read_text(encoding='utf-8').strip())
    required = {
        'books', 'dictionaries', 'grammars', 'peer-reviewed articles',
        'theses/dissertations', 'government/TRI/Census/LSI materials',
        'archives', 'newspapers/periodicals', 'web resources', 'datasets',
        'audio', 'video', 'maps', 'relevant media'
    }
    assert row['search_id'] == 'MMSC-SEARCH-000234'
    assert required.issubset(set(row['classes_searched']))
    census = row['official_census_reverification']
    assert census['reference_id'] == 'PC11_C16-18'
    assert census['metadata_verified'] is True
    assert census['bytes_acquired'] is False
    assert census['exact_cells_verified'] is False
    assert census['demographic_claim_promoted'] is False
    assert row['deduplication']['count_increment_permitted'] is False
    counts = row['counts']
    assert counts['audited_source_identities'] == 42
    assert counts['raw_web_discovery_records'] == 90
    assert counts['unique_web_discovery_leads'] == 87
    assert counts['duplicate_web_records'] == 3
    assert counts['canonicalized_unique_web_leads'] == 14
    assert counts['unresolved_unique_web_leads'] == 73
    assert counts['source_claims'] == 52
    assert counts['evidence_records'] == 52
    assert counts['evidence_links'] == 52
    assert counts['streamlit_modules'] == 42
    assert row['counts_changed'] is False
    assert row['release_gate'] == 'NOT_PASS'
