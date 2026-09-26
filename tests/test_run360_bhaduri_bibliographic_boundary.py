import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/bhaduri_mundari_english_dictionary_original_year_resolution_run360_2026-09-14.json"
SEARCH = ROOT / "audits/mmsc_search_run360_2026-09-14.json"


def test_run360_bhaduri_preferred_year_and_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["work"]["preferred_original_year_for_bibliographic_identity"] == 1931
    assert data["retained_anomaly"]["record"] == "BB09153012"
    assert "unresolved" in data["retained_anomaly"]["treatment"].lower()
    assert data["controlled_claims_added"] == 0
    assert data["controlled_evidence_records_added"] == 0
    assert data["controlled_counts_changed"] is False
    blocked = " ".join(data["not_verified"]).lower()
    for term in ("title page", "cryptographic hash", "ocr accuracy", "entry-level", "reuse rights", "community validation"):
        assert term in blocked


def test_run360_mmsc_counts_remain_conservative():
    data = json.loads(SEARCH.read_text(encoding="utf-8"))
    assert data["controlled_classes_refreshed"] == 14
    counts = data["controlled_counts_after_refresh"]
    assert counts == {
        "audited_source_identities": 42,
        "raw_web_discovery_records": 90,
        "unique_web_discovery_leads": 87,
        "duplicate_web_records": 3,
        "canonicalized_unique_web_leads": 14,
        "unresolved_unique_web_leads": 73,
    }
    assert data["count_change_this_run"] is False
