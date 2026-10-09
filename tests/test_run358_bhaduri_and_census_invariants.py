import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run358_bhaduri_is_bibliographic_only():
    data = load_json("data/source_census/bhaduri_mundari_english_dictionary_bibliographic_audit_run358_2026-09-14.json")
    assert data["promotion_level"] == "bibliographic identity, reprint genealogy and pagination concordance only"
    assert data["controlled_claims_added"] == 0
    assert data["controlled_evidence_records_added"] == 0
    assert data["controlled_counts_changed"] is False
    assert "dictionary entry-level text" in data["not_verified"]
    assert "reuse permission for any digitized manifestation" in data["not_verified"]


def test_run358_reprints_do_not_inflate_mmsc_counts():
    audit = load_json("audits/mmsc_search_run358_2026-09-14.json")
    assert audit["controlled_classes_refreshed"] == 14
    assert audit["count_change_this_run"] is False
    counts = audit["controlled_counts_after_refresh"]
    assert counts["audited_source_identities"] == 42
    assert counts["raw_web_discovery_records"] == 90
    assert counts["unique_web_discovery_leads"] == 87
    assert counts["duplicate_web_records"] == 3
    assert counts["canonicalized_unique_web_leads"] == 14
    assert counts["unresolved_unique_web_leads"] == 73
