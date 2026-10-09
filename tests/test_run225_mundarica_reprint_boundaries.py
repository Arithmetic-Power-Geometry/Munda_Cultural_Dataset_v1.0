import json
from pathlib import Path


def test_run225_mundarica_reprint_boundaries():
    p = Path('data/source_census/mundarica_reprint_volumes_xv_xvi_bibliographic_audit_run225_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 225
    assert data['branch'] == 'mlhkp-v2'
    records = {r['volume']: r for r in data['records']}
    assert records['XV']['isbn_13'] == '9788121203197'
    assert records['XVI']['isbn_13'] == '9788121203227'
    assert records['XV']['historical_original_manifestation_verified'] is False
    assert records['XVI']['historical_original_manifestation_verified'] is False
    assert data['cross_check']['individual_volume_16_vs_set_metadata_must_not_be_collapsed'] is True
    promotion = data['promotion']
    assert promotion['authoritative_registered_scan'] is False
    assert promotion['byte_integrity_verified'] is False
    assert promotion['ocr_verified'] is False
    assert promotion['verified_complete_volume'] is False
    assert promotion['public_cultural_claim_promoted'] is False
    assert promotion['community_validation_inferred'] is False
    assert promotion['cultural_access_permission_inferred'] is False
    assert data['deduplication']['count_increment_permitted'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'


def test_run225_search_log_exists_and_keeps_counts_frozen():
    p = Path('data/source_census/search_log_run225.jsonl')
    row = json.loads(p.read_text(encoding='utf-8').strip())
    assert row['search_id'] == 'MMSC-SEARCH-000225'
    assert row['counts_changed'] is False
    assert row['deduplication']['count_increment_permitted'] is False
    assert row['release_gate'] == 'NOT_PASS'
