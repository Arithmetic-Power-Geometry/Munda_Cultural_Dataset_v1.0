import json
from pathlib import Path


def test_run244_secondary_locator_never_becomes_verified_mundarica_content():
    p = Path("data/source_census/mundarica_vol_ii_iv_secondary_page_locator_run244_2026-09-12.json")
    data = json.loads(p.read_text(encoding="utf-8"))

    boundary = data["verification_boundary"]
    assert boundary["secondary_page_locator_verified"] is True
    assert boundary["underlying_mundarica_pages_directly_verified"] is False
    assert boundary["exact_historical_manifestation_verified"] is False
    assert boundary["lawful_complete_bytes_acquired"] is False
    assert boundary["independent_content_hash_verified"] is False
    assert boundary["ocr_verified"] is False
    assert boundary["cultural_claim_promoted"] is False
    assert boundary["passage_promoted"] is False

    promotion = data["promotion"]
    assert promotion["source_claims_added"] == 0
    assert promotion["evidence_records_added"] == 0
    assert promotion["evidence_links_added"] == 0

    governance = data["rights_access_governance"]
    assert governance["public_availability_treated_as_permission"] is False
    assert governance["community_validation_inferred"] is False
    assert governance["cultural_access_permission_inferred"] is False
    assert governance["cultural_access_overrides_entitlement"] is True
