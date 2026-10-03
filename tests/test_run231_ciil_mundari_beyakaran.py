import json
from pathlib import Path


def test_run231_ciil_mundari_beyakaran_boundaries():
    p = Path('data/source_census/ciil_sanchika_mundari_beyakaran_run231_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 231
    assert data['branch'] == 'mlhkp-v2'
    source = data['source']
    assert source['canonical_key'] == 'ciil:BVP03961'
    assert source['repository_identifier'] == 'BVP03961'
    assert source['author'] == 'Sikradas Tirki'
    assert source['year'] == 2015
    assert source['institutional_metadata_verified'] is True
    assert source['byte_preserving_download_acquired'] is False
    assert source['independent_hash_computed'] is False
    assert source['full_book_manifestation_verified'] is False
    assert source['claim_level_locator_promoted'] is False
    rights = data['rights_and_governance']
    assert rights['public_availability_treated_as_permission'] is False
    assert rights['rights_holder_metadata_treated_as_redistribution_license'] is False
    assert rights['community_validation_inferred'] is False
    assert rights['cultural_access_permission_inferred'] is False
    assert data['deduplication']['new_identity_count_increment_permitted'] is False
    assert data['promotion']['promoted_to_claim_evidence_graph'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'


def test_run231_all_class_search_log_and_counts_frozen():
    p = Path('data/source_census/search_log_run231.jsonl')
    row = json.loads(p.read_text(encoding='utf-8').strip())
    required = {
        'books', 'dictionaries', 'grammars', 'peer-reviewed articles',
        'theses/dissertations', 'government/TRI/Census/LSI materials',
        'archives', 'newspapers/periodicals', 'web resources', 'datasets',
        'audio', 'video', 'maps', 'relevant media'
    }
    assert row['search_id'] == 'MMSC-SEARCH-000231'
    assert required.issubset(set(row['classes_searched']))
    assert row['deduplication']['count_increment_permitted'] is False
    assert row['counts']['audited_source_identities'] == 42
    assert row['counts']['raw_web_discovery_records'] == 90
    assert row['counts']['unique_web_discovery_leads'] == 87
    assert row['counts']['duplicate_web_records'] == 3
    assert row['counts']['canonicalized_unique_web_leads'] == 14
    assert row['counts']['unresolved_unique_web_leads'] == 73
    assert row['counts']['source_claims'] == 52
    assert row['counts']['evidence_records'] == 52
    assert row['counts']['evidence_links'] == 52
    assert row['counts']['streamlit_modules'] == 42
    assert row['counts_changed'] is False
    assert row['release_gate'] == 'NOT_PASS'
