import json
from pathlib import Path


def test_run220_lsi_pari_secondary_manifestation_boundary():
    p = Path('data/source_census/lsi_jharkhand_pari_secondary_manifestation_run220_2026-09-11.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 220
    assert data['branch'] == 'mlhkp-v2'
    assert data['exact_locator']['mundari_factoid_number'] == 5
    assert data['verification_boundary']['secondary_manifestation_identity_verified'] is True
    assert data['verification_boundary']['official_pdf_bytes_verified'] is False
    assert data['verification_boundary']['official_pdf_independent_hash_verified'] is False
    assert data['verification_boundary']['numeric_or_linguistic_claim_promoted_to_public_evidence_graph'] is False
    assert data['rights_governance']['public_availability_treated_as_permission'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'
