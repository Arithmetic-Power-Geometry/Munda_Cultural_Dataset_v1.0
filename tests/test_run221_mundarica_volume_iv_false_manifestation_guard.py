import json
from pathlib import Path


def test_run221_mundarica_volume_iv_false_manifestation_guard():
    p = Path('data/source_census/mundarica_volume_iv_false_manifestation_guard_run221_2026-09-11.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 221
    assert data['branch'] == 'mlhkp-v2'
    assert data['direct_manifestation_identity']['internet_archive_identifier'] == 'in.ernet.dli.2015.14921'
    assert data['direct_manifestation_identity']['displayed_title'] == 'Encyclopedia Mundarica Vol-iii (1930)'
    assert data['deterministic_disposition']['canonical_volume_for_this_identifier'] == 'III'
    assert data['deterministic_disposition']['may_be_used_as_volume_iv_manifestation'] is False
    assert data['verification_boundary']['volume_iv_exact_manifestation_verified_by_this_record'] is False
    assert data['verification_boundary']['ocr_verified'] is False
    assert data['rights_governance']['public_availability_treated_as_permission'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'
