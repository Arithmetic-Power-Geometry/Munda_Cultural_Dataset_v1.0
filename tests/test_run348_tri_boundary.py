import json
from pathlib import Path


def test_run348_tri_promotion_boundary():
    p = Path("data/source_census/tri_munda_official_locator_run348_2026-09-14.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    v = d["verification"]
    assert v["provider_page_identity_verified"] is True
    assert v["government_institution_context_verified"] is True
    assert v["page_content_independently_field_verified"] is False
    assert v["community_validation_verified"] is False
    assert v["cultural_access_authorization_inferred"] is False
    assert v["reuse_license_verified_for_page_content"] is False
    assert d["rights_and_governance"]["cultural_access_overrides_entitlement"] is True
    assert d["deduplication"]["count_change_authorized"] is False


def test_run348_search_log_covers_all_controlled_classes():
    p = Path("audits/mmsc_search_run348_2026-09-14.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["classes_refreshed"] == 14
    assert len(d["classes"]) == 14
    assert d["controlled_counts_changed"] is False
    assert d["controlled_counts"]["unresolved_unique_web_leads"] == 73
