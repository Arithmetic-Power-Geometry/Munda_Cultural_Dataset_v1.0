import json
from pathlib import Path


def test_run232_wikimedia_map_rights_and_primary_evidence_boundary():
    p = Path('data/source_census/wikimedia_mundari_assam_distribution_map_run232_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 232
    assert data['branch'] == 'mlhkp-v2'
    source = data['source']
    assert source['canonical_key'] == 'commons:File:Mundari_language_distribution_-_Assam.svg'
    assert source['author'] == 'MaxA-Matrix'
    assert source['date'] == '2024-06-28'
    assert source['media_type'] == 'image/svg+xml'
    assert source['metadata_manifestation_verified'] is True
    assert source['file_history_manifestation_verified'] is True
    assert source['byte_preserving_download_acquired'] is False
    assert source['independent_hash_computed'] is False
    assert source['underlying_census_workbook_verified'] is False
    rights = data['rights_and_governance']
    assert rights['license'] == 'CC BY-SA 4.0'
    assert rights['sharing_and_adaptation_permitted_subject_to_license'] is True
    assert rights['demographic_claim_promoted_from_secondary_map'] is False
    assert rights['community_validation_inferred'] is False
    assert rights['cultural_access_permission_inferred'] is False
    promotion = data['promotion']
    assert promotion['promoted_beyond_discovery_only'] is True
    assert promotion['promoted_to_claim_evidence_graph'] is False
    assert promotion['demographic_value_promoted'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'


def test_run232_all_class_log_and_counts_remain_synchronized():
    p = Path('data/source_census/search_log_run232.jsonl')
    row = json.loads(p.read_text(encoding='utf-8').strip())
    required = {
        'books', 'dictionaries', 'grammars', 'peer-reviewed articles',
        'theses/dissertations', 'government/TRI/Census/LSI materials',
        'archives', 'newspapers/periodicals', 'web resources', 'datasets',
        'audio', 'video', 'maps', 'relevant media'
    }
    assert row['search_id'] == 'MMSC-SEARCH-000232'
    assert required.issubset(set(row['classes_searched']))
    assert row['rights_boundary']['license'] == 'CC BY-SA 4.0'
    assert row['rights_boundary']['secondary_map_not_substituted_for_primary_census_evidence'] is True
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
