import json
from pathlib import Path


def test_wals_mundari_source_boundary_is_non_promotional():
    p = Path("audits/wals_mundari_source_boundary_run352_2026-09-14.json")
    data = json.loads(p.read_text(encoding="utf-8"))

    assert data["source"]["wals_code"] == "mun"
    assert data["source"]["iso_639_3"] == "unr"
    assert data["source"]["provider_role"] == "secondary typological database"
    assert data["verification_boundary"]["wals_feature_values_independently_source_verified"] is False
    assert data["verification_boundary"]["feature_level_provenance_chain_complete"] is False
    assert data["promotion"]["feature_values_promoted"] == 0
    assert data["promotion"]["linguistic_claims_promoted"] == 0
    assert data["promotion"]["cultural_claims_promoted"] == 0
    assert data["promotion"]["evidence_graph_count_change"] == 0
    assert data["governance"]["cultural_access_overrides_entitlement"] is True
    assert data["governance"]["public_feature_value_requires_underlying_source_resolution"] is True
