import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run192_unicode_reconciles_without_count_or_rights_inflation():
    audit = load_json("data/source_census/unicode_nag_mundari_existing_identity_reconciliation_run192_2026-09-11.json")
    master = load_json("data/source_census/mmsc_discoveries.json")

    assert audit["result"] == "EXISTING_IDENTITY_CONFIRMED_NO_NEW_SOURCE"
    assert audit["existing_source"]["source_id"] == "SRC-MMSC-000011"
    assert audit["existing_source"]["identifier"]["value"] == "17.0.0/13.12"
    assert audit["run191_locator"]["block_range"] == "U+1E4D0-U+1E4FF"

    identities = [r for r in master if r.get("source_id") == "SRC-MMSC-000011"]
    assert len(identities) == 1
    identity = identities[0]
    assert identity["title"] == "The Unicode Standard, Version 17.0 — Nag Mundari"
    assert identity["identifier"]["value"] == "17.0.0/13.12"

    effect = audit["count_effect"]
    assert effect["source_identity_added"] is False
    for key, value in effect.items():
        if key.endswith("_delta"):
            assert value == 0

    rights = audit["rights_and_governance"]
    assert rights["public_availability_treated_as_permission"] is False
    assert rights["chart_or_font_bytes_ingested"] is False
    assert rights["glyph_images_redistributed"] is False
    assert rights["participant_consent_inferred"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_inferred"] is False
    assert rights["cultural_access_overrides_entitlement"] is True


def test_run192_release_counts_remain_defensible():
    status = load_json("status/mlhkp_progress.json")
    assert status["latest_run"] >= 191
    assert status["mmsc"]["audited_source_identities"] == 42
    assert status["mmsc"]["raw_web_discovery_records"] == 90
    assert status["mmsc"]["unique_web_discovery_leads"] == 87
    assert status["mmsc"]["duplicate_web_records"] == 3
    assert status["mmsc"]["canonicalized_unique_web_leads"] == 14
    assert status["mmsc"]["unresolved_unique_web_leads"] == 73
    assert status["evidence_and_schema"]["source_claims"] == 52
    assert status["evidence_and_schema"]["evidence_records"] == 52
    assert status["evidence_and_schema"]["evidence_links"] == 52
    assert status["release_gate"]["status"] == "NOT_PASS"
