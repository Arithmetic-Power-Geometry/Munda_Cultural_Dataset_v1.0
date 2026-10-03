import json
from pathlib import Path


def test_run223_glottolog_mundari_identity_boundary():
    p = Path('data/source_census/glottolog_mundari_identity_boundary_run223_2026-09-12.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['run'] == 223
    assert data['branch'] == 'mlhkp-v2'
    assert data['active_identity']['name'] == 'Mundari'
    assert data['active_identity']['glottocode'] == 'mund1320'
    assert data['active_identity']['iso_639_3'] == 'unr'
    assert data['retired_identity']['name'] == 'Munda'
    assert data['retired_identity']['glottocode'] == 'mund1321'
    assert data['retired_identity']['iso_639_3'] == 'unx'
    assert data['canonicalization_rule']['collapse_active_and_retired_records'] is False
    assert data['rights_governance']['public_availability_treated_as_cultural_access_permission'] is False
    assert data['rights_governance']['community_validation_inferred'] is False
    assert data['verification_boundary']['cultural_claim_promoted_to_public_evidence_graph'] is False
    assert data['verification_boundary']['source_identity_count_changed'] is False
    assert data['release_effect']['counts_changed'] is False
    assert data['release_effect']['release_gate'] == 'NOT_PASS'
