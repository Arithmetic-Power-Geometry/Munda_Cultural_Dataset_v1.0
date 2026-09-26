import json
from pathlib import Path


def _audit():
    path = Path("audits/sinha_1975_bibliographic_pagination_concordance_run356_2026-09-14.json")
    return json.loads(path.read_text(encoding="utf-8"))


def test_sinha_bibliographic_concordance_does_not_imply_digital_verification():
    audit = _audit()
    findings = audit["findings"]
    assert findings["bibliographic_identity_concordant"] is True
    assert findings["bibliographic_pagination_concordant"] is True
    assert findings["digital_manifestation_size_concordant"] is False
    assert findings["digital_manifestation_bytes_verified"] is False
    assert findings["sha256_verified"] is False
    assert findings["page_image_to_print_page_concordance_verified"] is False
    assert findings["full_text_or_ocr_verified"] is False


def test_sinha_source_not_promoted_without_rights_and_locator_verification():
    audit = _audit()
    findings = audit["findings"]
    boundary = audit["promotion_boundary"]
    assert findings["reuse_license_verified"] is False
    assert findings["community_validation_verified"] is False
    assert findings["cultural_access_authorization_verified"] is False
    assert boundary["public_linguistic_claims_promoted"] == 0
    assert boundary["public_cultural_claims_promoted"] == 0
