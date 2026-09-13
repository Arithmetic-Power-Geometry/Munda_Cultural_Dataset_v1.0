import json
from pathlib import Path


def test_run321_mundarica_manifestation_boundaries():
    data = json.loads(Path('data/source_census/mundarica_manifestation_audit_run321_2026-09-14.json').read_text())
    assert data['run'] == 321
    assert {m['volume'] for m in data['manifestations']} == {'II', 'III'}
    assert all(m['archive_page_verified'] for m in data['manifestations'])
    assert all(not m['bytes_acquired_independently'] for m in data['manifestations'])
    assert all(not m['hash_recomputed'] for m in data['manifestations'])
    assert all(not m['page_image_concordance_verified'] for m in data['manifestations'])
    assert all(m['ocr_pages_verified'] == 0 for m in data['manifestations'])
    assert all(not m['verified_complete_volume'] for m in data['manifestations'])
    assert all(m['claims_promoted'] == 0 for m in data['manifestations'])


def test_run321_mmsc_class_refresh():
    data = json.loads(Path('data/source_census/mmsc_search_run321_2026-09-14.json').read_text())
    assert data['search_id'] == 'MMSC-SEARCH-000321'
    assert data['controlled_classes_refreshed'] == 14
    assert len(data['classes']) == 14
    assert data['count_effect']['counts_changed_this_run'] is False
