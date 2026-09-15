import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run357_locator_is_metadata_only():
    data = load_json("data/source_census/wikimedia_munda_languages_map_exact_locator_run357_2026-09-14.json")
    assert data["controlled_claims_added"] == 0
    assert data["controlled_evidence_records_added"] == 0
    assert data["controlled_counts_changed"] is False
    assert data["records"][0]["promotion_level"] == "exact provider locator, manifestation metadata and licence only"


def test_run357_census_keeps_controlled_counts_stable():
    audit = load_json("audits/mmsc_search_run357_2026-09-14.json")
    assert audit["controlled_classes_refreshed"] == 14
    assert audit["count_change_this_run"] is False
    counts = audit["controlled_counts_after_refresh"]
    assert counts["audited_source_identities"] == 42
    assert counts["unresolved_unique_web_leads"] == 73
