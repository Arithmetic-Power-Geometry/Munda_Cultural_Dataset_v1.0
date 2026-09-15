import json
from pathlib import Path


AUDIT = Path("data/source_census/mundarica_xi_xii_historical_bibliographic_audit_run325_2026-09-14.json")


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run325_historical_pagination_is_recorded_exactly():
    audit = load_audit()
    obs = audit["observations"]
    assert audit["run"] == 325
    assert audit["branch"] == "mlhkp-v2"
    assert obs["volume_xi"]["publication_year"] == 1938
    assert obs["volume_xi"]["printed_page_range"] == "3175-3456"
    assert obs["volume_xii"]["publication_year"] == 1938
    assert obs["volume_xii"]["printed_page_range"] == "3457-3707"


def test_run325_bibliographic_anchor_cannot_be_promoted_to_scan_or_ocr_completion():
    audit = load_audit()
    boundary = audit["verification_boundary"]
    obs = audit["observations"]
    assert audit["source"]["primary_scan_bytes_acquired"] is False
    assert audit["source"]["independent_hash_verified"] is False
    assert obs["volume_xi"]["scan_image_concordance_verified"] is False
    assert obs["volume_xi"]["ocr_verified"] is False
    assert obs["volume_xii"]["scan_image_concordance_verified"] is False
    assert obs["volume_xii"]["ocr_verified"] is False
    assert boundary["authoritative_registered_scans_added"] == 0
    assert boundary["verified_complete_volumes_added"] == 0
    assert boundary["verified_ocr_pages_added"] == 0
    assert boundary["content_level_claims_promoted"] == 0
