import json
from pathlib import Path

P = Path('data/source_census/rau_2019_zenodo_manifestation_audit_run316_2026-09-13.json')


def test_run316_rau_manifestation_boundary():
    d = json.loads(P.read_text(encoding='utf-8'))
    assert d['doi'] == '10.5281/zenodo.3380874'
    assert d['filename'] == 'pMunda_cognate_set_2019-08-29.csv'
    assert d['publisher_declared_md5'] == '07e1d945a0fc6cafc4fc7afd3f1ff144'
    assert d['declared_cognate_sets'] == 127
    assert d['mundari_included'] is True
    assert d['exact_manifestation_locator_verified'] is True
    assert d['bytes_independently_acquired'] is False
    assert d['independent_hash_recomputed'] is False
    assert d['explicit_license_text_verified'] is False
    assert d['reuse_permission_inferred'] is False
    assert d['controlled_claim_count_increment'] == 0
    assert d['controlled_evidence_count_increment'] == 0
    assert d['linguistic_rows_promoted'] == 0
    assert d['cultural_claims_promoted'] == 0
