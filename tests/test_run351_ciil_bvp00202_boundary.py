import json
from pathlib import Path

AUDIT = Path("audits/ciil_mundari_grammar_bvp00202_run351_2026-09-14.json")


def test_ciil_exact_locator_does_not_overstate_verification():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    v = data["verification"]
    g = data["governance"]
    assert data["provider_identifier"] == "BVP00202"
    assert v["first_party_item_metadata_verified"] is True
    assert v["bitstream_endpoint_resolved"] is True
    assert v["independent_binary_download_succeeded"] is False
    assert v["independent_sha256_verified"] is False
    assert v["full_page_count_verified"] is False
    assert v["linguistic_claims_promoted"] == 0
    assert v["cultural_claims_promoted"] == 0
    assert g["public_availability_is_reuse_permission"] is False
    assert g["rights_holder_metadata_is_license_grant"] is False
    assert g["community_validation_verified"] is False
    assert g["cultural_access_authorized"] is False
    assert g["promotion_allowed"] is False
