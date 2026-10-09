import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "sapienza_adivasi_womens_movements_exact_locator_run343_2026-09-14.json"


def test_sapienza_locator_does_not_promote_unverified_content_or_language_authority():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["scope"]["scope_level"] == "contextual_munda_community_source"
    assert data["scope"]["promotion_state"] == "exact_locator_metadata_only"
    assert "Mundari grammar" in data["scope"]["not_authority_for"]
    assert data["manifestation"]["local_bytes_acquired"] is False
    assert data["manifestation"]["independent_sha256_verified"] is False
    assert data["rights_governance"]["reuse_rights_fully_resolved"] is False
    assert data["rights_governance"]["participant_consent_verified"] is False
    assert data["rights_governance"]["community_validation_verified"] is False
    assert data["rights_governance"]["cultural_access_authorization_verified"] is False
    assert data["evidence_boundary"]["public_cultural_claims_promoted"] == 0
    assert data["evidence_boundary"]["public_linguistic_claims_promoted"] == 0
    assert data["evidence_boundary"]["controlled_graph_records_added"] == 0
