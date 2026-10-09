import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "mundarica_manifestation_reconciliation_run309_2026-09-13.json"
SEARCH_LOG = ROOT / "data" / "source_census" / "search_log_run309.jsonl"


def _audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run309_manifestations_are_not_collapsed():
    d = _audit()
    assert "must not be collapsed" in d["deduplication_rule"]
    v13 = next(x for x in d["source_checks"] if x.get("volume") == 13)
    v16 = next(x for x in d["source_checks"] if x.get("volume") == 16)
    assert v13["year"] == 1941
    assert v13["publisher"] == "Superintendent government printing, Bihar and Orissa"
    assert v16["reported_pages_conflict"] == [43, 96]


def test_run309_does_not_false_verify_scans_or_ocr():
    b = _audit()["verification_boundary"]
    assert b["authoritative_registered_scans_added"] == 0
    assert b["verified_complete_volumes_added"] == 0
    assert b["ocr_verified_pages_added"] == 0
    assert b["cultural_claims_promoted"] == 0
    assert b["controlled_evidence_records_promoted"] == 0
    assert b["modern_reprint_pagination_used_as_historical_scan_pagination"] is False
    assert b["volume16_pagination_conflict_resolved"] is False


def test_run309_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in SEARCH_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert {r["class"] for r in rows} == {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers", "web_resources", "datasets", "audio", "video",
        "maps", "relevant_media"
    }
