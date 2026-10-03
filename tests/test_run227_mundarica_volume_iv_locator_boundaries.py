import json
from pathlib import Path


def test_run227_mundarica_volume_iv_secondary_locator_boundaries():
    p = Path('data/source_census/mundarica_volume_iv_secondary_page_locator_audit_run227_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 227
    assert data['branch'] == 'mlhkp-v2'
    locator = data['directly_observed_reference_entry']['volume_iv_locator']
    assert locator['volume_label'] == 'Vol. IV-D'
    assert locator['entry_term'] == 'deonra'
    assert locator['printed_page_range'] == '1022-1039'
    reconciliation = data['reconciliation']
    assert reconciliation['known_bad_volume_iv_archive_alias'] == 'in.ernet.dli.2015.14921'
    assert reconciliation['known_bad_alias_resolves_to'] == 'Volume III'
    assert reconciliation['volume_iv_exact_digital_manifestation_verified_this_run'] is False
    promotion = data['promotion']
    assert promotion['secondary_bibliographic_page_locator_verified'] is True
    assert promotion['exact_volume_iv_digital_manifestation_verified'] is False
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


def test_run227_search_log_exists_and_keeps_counts_frozen():
    p = Path('data/source_census/search_log_run227.jsonl')
    row = json.loads(p.read_text(encoding='utf-8').strip())
    assert row['search_id'] == 'MMSC-SEARCH-000227'
    assert row['counts_changed'] is False
    assert row['deduplication']['count_increment_permitted'] is False
    assert row['release_gate'] == 'NOT_PASS'
