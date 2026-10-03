import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/mundarica_xi_xii_bibliographic_page_range_audit_run270_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run270.jsonl"


def test_run270_mundarica_xi_xii_ranges_are_bibliographic_only():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["bibliographic_observation"]["volume_xi"]["printed_page_range"] == "3175-3456"
    assert d["bibliographic_observation"]["volume_xii"]["printed_page_range"] == "3457-3707"
    assert d["bibliographic_observation"]["volume_xi"]["range_span_inclusive"] == 282
    assert d["bibliographic_observation"]["volume_xii"]["range_span_inclusive"] == 251
    b = d["verification_boundary"]
    assert b["printed_page_range_bibliographically_verified"] is True
    assert b["scan_bytes_verified"] is False
    assert b["independent_hash_verified"] is False
    assert b["scan_completeness_verified"] is False
    assert b["ocr_verified"] is False


def test_run270_no_false_rights_or_cultural_promotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    b = d["verification_boundary"]
    assert b["redistribution_permission_inferred"] is False
    assert b["model_training_permission_inferred"] is False
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False
    assert b["cultural_facts_promoted"] == 0
    assert d["release_effect"]["verified_complete_volumes_change"] == 0


def test_run270_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000270" for r in rows)
