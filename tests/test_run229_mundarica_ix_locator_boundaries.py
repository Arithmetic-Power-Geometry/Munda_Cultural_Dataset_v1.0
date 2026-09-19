import json
from pathlib import Path


def test_run229_mundarica_ix_secondary_locator_boundary():
    p = Path('data/source_census/mundarica_volume_ix_supreme_court_secondary_locator_run229_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 229
    assert data['branch'] == 'mlhkp-v2'
    assert data['source']['mundarica_reference']['volume'] == 'IX'
    assert set(data['source']['mundarica_reference']['secondary_printed_page_locators']) == {2756, 2881}
    assert data['identity_verification']['supreme_court_judgment_identity_verified'] is True
    assert data['locator_state']['secondary_page_locator_verified'] is True
    assert data['locator_state']['exact_volume_ix_digital_manifestation_verified'] is False
    assert data['locator_state']['authoritative_scan_registered'] is False
    assert data['locator_state']['bitstream_bytes_acquired'] is False
    assert data['locator_state']['independent_hash_computed'] is False
    assert data['locator_state']['ocr_verified'] is False
    assert data['locator_state']['volume_complete_verified'] is False
    assert data['rights_and_governance']['judgment_visibility_treated_as_mundarica_reuse_permission'] is False
    assert data['rights_and_governance']['community_validation_inferred'] is False
    assert data['promotion']['promoted_to_claim_evidence_graph'] is False
    assert data['promotion']['cultural_claim_promoted'] is False
    assert data['deduplication']['new_source_identity_count_increment_permitted'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'


def test_run229_all_class_search_log_and_counts_frozen():
    p = Path('data/source_census/search_log_run229.jsonl')
    row = json.loads(p.read_text(encoding='utf-8').strip())
    required = {
        'books', 'dictionaries', 'grammars', 'peer-reviewed articles',
        'theses/dissertations', 'government/TRI/Census/LSI materials',
        'archives', 'newspapers/periodicals', 'web resources', 'datasets',
        'audio', 'video', 'maps', 'relevant media'
    }
    assert row['search_id'] == 'MMSC-SEARCH-000229'
    assert required.issubset(set(row['classes_searched']))
    assert row['deduplication']['count_increment_permitted'] is False
    assert row['counts']['audited_source_identities'] == 42
    assert row['counts']['unresolved_unique_web_leads'] == 73
    assert row['counts']['source_claims'] == 52
    assert row['counts']['evidence_records'] == 52
    assert row['counts']['evidence_links'] == 52
    assert row['counts']['streamlit_modules'] == 42
    assert row['counts_changed'] is False
    assert row['release_gate'] == 'NOT_PASS'
