import json
from pathlib import Path


def test_run248_mundarica_googlebooks_boundary():
    p = Path("data/source_census/mundarica_volumes_3_5_googlebooks_nypl_manifestation_run248_2026-09-12.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["run_id"] == 248
    assert data["work"]["google_books_id"] == "H3T9md87HvcC"
    assert data["work"]["year_displayed"] == 1930
    assert data["work"]["original_from_displayed"] == "the New York Public Library"
    assert data["rights_access_boundary"]["full_text_bytes_acquired"] is False
    assert data["rights_access_boundary"]["cryptographic_hash_verified"] is False
    assert data["rights_access_boundary"]["scan_sequence_verified"] is False
    assert data["rights_access_boundary"]["ocr_verified"] is False
    assert data["content_evidence_promoted"] is False
    assert data["passages_promoted"] == 0
    assert data["claims_promoted"] == 0
    assert data["identity_count_change"] is False
    assert data["evidence_claim_count_change"] is False
    assert set(data["volume_effect"]) == {"III", "IV", "V"}


def test_run248_search_log_covers_requested_classes():
    p = Path("data/source_census/search_log_run248.jsonl")
    rows = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {r["class"] for r in rows}
    required = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert required.issubset(classes)
    assert {r["search_id"] for r in rows} == {"MMSC-SEARCH-000248"}
