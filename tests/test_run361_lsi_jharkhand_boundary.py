import json
from pathlib import Path


def test_run361_lsi_jharkhand_locator_is_not_content_verification():
    p = Path("data/source_census/lsi_jharkhand_exact_locator_run361_2026-09-14.json")
    data = json.loads(p.read_text(encoding="utf-8"))

    assert data["identity_verification"]["provider_catalogue_verified"] is True
    assert data["identity_verification"]["provider_declared_filename_verified"] is True
    assert data["access_verification"]["local_pdf_bytes_obtained"] is False
    assert data["access_verification"]["sha256_verified"] is False
    assert data["access_verification"]["page_inventory_verified"] is False
    assert data["access_verification"]["exact_internal_mundari_page_locator_verified"] is False
    assert data["rights_governance"]["reuse_permission_inferred"] is False
    assert data["rights_governance"]["participant_consent_verified"] is False
    assert data["rights_governance"]["community_validation_verified"] is False
    assert data["rights_governance"]["cultural_access_authorization_verified"] is False
    assert data["scope_classification"]["controlled_linguistic_claims_promoted"] == 0
    assert data["scope_classification"]["controlled_cultural_claims_promoted"] == 0
    assert data["scope_classification"]["numeric_claims_promoted"] == 0
