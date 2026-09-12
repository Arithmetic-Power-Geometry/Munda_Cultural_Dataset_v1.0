import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/birsaite_dharam_exact_locator_audit_2026-09-10.json"


def test_run160_birsaite_exact_locator_and_governance_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["web_source_id"] == "WEB-MUN-0082"
    assert data["source_identity"]["doi"] == "10.1080/14631369.2025.2589154"
    assert data["source_identity"]["pages"] == "631-654"
    assert data["publisher_page_verification"]["identity_and_pagination_verified"] is True
    assert data["publisher_page_verification"]["abstract_verified"] is True
    assert data["scope_boundary"]["participant_derived_material_ingested"] is False
    assert data["scope_boundary"]["ritual_or_sensitive_cultural_detail_ingested"] is False
    rights = data["rights_governance"]
    assert rights["participant_consent_for_MLHKP_secondary_use_verified"] is False
    assert rights["community_validation_for_MLHKP_verified"] is False
    assert rights["cultural_access_clearance_verified"] is False
    assert rights["cultural_access_overrides_technical_or_legal_entitlement"] is True
    decision = data["canonicalization_decision"]
    assert decision["status"] == "exact_identity_and_locator_verified_but_permanent_identity_promotion_deferred"
    assert decision["unresolved_lead_count_changed"] is False
