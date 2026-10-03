import json
from pathlib import Path


def test_run379_ncert_barkhaa_promotion_boundary():
    p = Path("data/source_census/ncert_barkhaa_mundari_audio_exact_locator_run379_2026-09-15.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["promotion_state"] == "exact_provider_locator_discovery_only"
    g = d["rights_access_consent_cultural_state"]
    assert g["item_level_reuse_permission_verified"] is False
    assert g["audio_bytes_materialized"] is False
    assert g["sha256_verified"] is False
    assert g["speaker_consent_verified"] is False
    assert g["community_validation_verified"] is False
    assert g["cultural_access_authorization_verified"] is False
    boundary = d["promotion_boundary"].lower()
    assert "no audio" in boundary
    assert "cultural claim" in boundary


def test_run379_search_keeps_one_provider_family_identity():
    p = Path("audits/mmsc_search_run379_2026-09-15.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["controlled_classes_refreshed"] == 14
    assert d["deduplication"]["new_raw_records"] == 1
    assert d["deduplication"]["new_unique_leads"] == 1
    assert d["deduplication"]["new_duplicates"] == 0
    assert d["public_factual_claims_promoted"] == 0
    assert d["cultural_claims_promoted"] == 0
