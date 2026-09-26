import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(relative_path: str):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def test_phoible_secondary_inventory_not_promoted():
    audit = _load("audits/phoible_mundari_source_boundary_run354_2026-09-14.json")
    boundary = audit["verification_boundary"]
    governance = audit["rights_governance"]

    assert boundary["database_record_verified"] is True
    assert boundary["underlying_descriptive_sources_independently_verified"] is False
    assert boundary["inventory_values_promoted_to_controlled_claims"] is False
    assert boundary["phonological_claims_promoted"] == 0
    assert boundary["cultural_claims_promoted"] == 0
    assert governance["database_license_does_not_establish_underlying_source_reuse_rights"] is True
    assert governance["database_license_does_not_establish_community_validation"] is True
    assert governance["database_license_does_not_establish_cultural_access_authorization"] is True
    assert governance["cultural_access_overrides_entitlement"] is True


def test_mundarica_reprint_locator_not_ocr_completion():
    audit = _load("audits/mundarica_xv_xvi_reprint_locator_run354_2026-09-14.json")
    boundary = audit["verification_boundary"]

    assert boundary["bibliographic_reprint_locator_verified"] is True
    assert boundary["historical_primary_manifestation_verified"] is False
    assert boundary["printed_page_to_scan_image_concordance_verified"] is False
    assert boundary["ocr_verified_pages"] == 0
    assert boundary["complete_volume_verified"] is False
    assert boundary["content_claims_promoted"] == 0


def test_run354_census_counts_are_not_inflated_by_discovery():
    census = _load("audits/mmsc_search_run354_2026-09-14.json")
    counts = census["controlled_counts_after_refresh"]

    assert census["count_change"] is False
    assert counts == {
        "audited_source_identities": 42,
        "raw_web_discovery_records": 90,
        "unique_web_discovery_leads": 87,
        "duplicate_web_records": 3,
        "canonicalized_unique_web_leads": 14,
        "unresolved_unique_web_leads": 73,
    }
    assert census["homonym_and_scope_controls"]["do_not_promote_search_hit_to_audited_identity"] is True
