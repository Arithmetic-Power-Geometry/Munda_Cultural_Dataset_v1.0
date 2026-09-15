import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/mundarica_volume_xii_reprint_locator_run278_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run278.jsonl"


def test_run278_volume_xii_reprint_identity_is_exact_but_manifestation_limited():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    s = d["source"]
    assert d["volume"] == "XII"
    assert s["manifestation_type"] == "modern commercial reprint"
    assert s["publication_year"] == 2009
    assert s["isbn_13"] == "9788121203166"
    assert s["isbn_10"] == "8121203163"
    assert s["reported_print_length_pages"] == 250
    assert d["existing_historical_bibliographic_state"]["printed_page_range"] == "3457-3707"
    assert d["existing_historical_bibliographic_state"]["equated_to_reprint_pagination"] is False


def test_run278_does_not_promote_reprint_to_scan_ocr_or_completeness():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    p = d["promotion"]
    i = d["integrity_boundary"]
    assert p["authoritative_registered_scan_count_change"] is False
    assert p["verified_complete_volume_count_change"] is False
    assert p["ocr_verified"] is False
    assert p["historical_scan_bytes_acquired"] is False
    assert p["claims_added"] == 0
    assert p["evidence_records_added"] == 0
    assert i["independent_hash_computed"] is False
    assert i["printed_page_to_scan_image_concordance_verified"] is False
    assert i["completeness_verified"] is False


def test_run278_no_rights_or_cultural_permission_inference():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    b = d["rights_and_cultural_boundary"]
    assert b["commercial_availability_treated_as_redistribution_permission"] is False
    assert b["reprint_listing_treated_as_model_training_permission"] is False
    assert b["community_validation_verified"] is False
    assert b["cultural_access_permission_verified"] is False
    assert b["cultural_access_overrides_technical_or_legal_entitlement"] is True


def test_run278_search_log_covers_all_controlled_classes_once():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert len(rows) == 14
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000278" for r in rows)
