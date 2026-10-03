import json
from pathlib import Path


def test_run222_tri_jharkhand_munda_official_html_boundary():
    p = Path('data/source_census/tri_jharkhand_munda_official_html_locator_run222_2026-09-11.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 222
    assert data['branch'] == 'mlhkp-v2'
    assert data['source_identity']['manifestation_type'] == 'official TRI HTML ethnographic page'
    assert data['exact_locators']['literature_and_studies_section_observed'] is True
    assert data['verification_boundary']['official_institutional_manifestation_verified'] is True
    assert data['verification_boundary']['section_level_exact_locator_verified'] is True
    assert data['verification_boundary']['cultural_claim_promoted_to_public_evidence_graph'] is False
    assert data['rights_governance']['public_availability_treated_as_permission'] is False
    assert data['rights_governance']['community_validation_inferred'] is False
    assert data['canonicalization']['new_audited_source_identity_count_asserted'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'
