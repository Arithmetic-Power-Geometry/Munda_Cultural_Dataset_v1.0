import json
from pathlib import Path


def test_scstrti_locator_does_not_overclaim_content_or_rights():
    p = Path("data/source_census/scstrti_mundari_handbook_exact_locator_run369_2026-09-15.json")
    d = json.loads(p.read_text(encoding="utf-8"))

    assert d["record_id"] == "SCST/2016/0055"
    assert d["file"]["name"] == "SCST_2016_handbook_0055.pdf"
    assert d["identity_verification"]["official_repository_record_verified"] is True
    assert d["identity_verification"]["exact_file_locator_verified"] is True

    assert d["file"]["binary_materialized"] is False
    assert d["file"]["sha256_verified"] is False
    assert d["file"]["page_count_from_binary_verified"] is False

    assert d["rights_governance"]["provider_visibility_does_not_equal_reuse_permission"] is True
    assert d["rights_governance"]["item_level_reuse_license_verified"] is False
    assert d["rights_governance"]["community_validation_verified"] is False
    assert d["rights_governance"]["cultural_access_authorization_verified"] is False

    assert d["evidence_promotion"]["new_controlled_cultural_claims"] == 0
    assert d["evidence_promotion"]["new_controlled_linguistic_claims"] == 0
    assert d["evidence_promotion"]["exact_locator_evidence_only"] is True
