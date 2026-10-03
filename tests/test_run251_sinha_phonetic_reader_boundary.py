import json
from pathlib import Path


def test_run251_sinha_phonetic_reader_boundary():
    p = Path("data/source_census/sinha_1974_mundari_phonetic_reader_exact_locator_run251_2026-09-12.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["run_id"] == 251
    assert data["work"]["canonical_title"] == "Mundari Phonetic Reader"
    assert data["work"]["author"] == "N. K. Sinha"
    assert data["work"]["year"] == 1974
    assert data["work"]["series_number"] == 13
    ids = {x.get("book_id") for x in data["verified_locators"] if x["provider"] == "Google Books"}
    assert {"hITRAAAAMAAJ", "Rn8KAQAAIAAJ"}.issubset(ids)
    assert any(x.get("record_id") == "BA72929895" for x in data["verified_locators"])
    assert data["deduplication"]["canonical_key"] == "sinha-nk|1974|mundari-phonetic-reader|ciil-series-13"
    assert data["deduplication"]["identity_count_change"] is False
    assert len(data["metadata_conflicts"]) >= 1
    assert data["rights_access_boundary"]["full_text_bytes_acquired"] is False
    assert data["rights_access_boundary"]["cryptographic_hash_verified"] is False
    assert data["rights_access_boundary"]["scan_sequence_to_printed_pagination_verified"] is False
    assert data["rights_access_boundary"]["ocr_verified"] is False
    assert data["promotion"]["content_evidence_promoted"] is False
    assert data["promotion"]["lexical_rows_promoted"] == 0
    assert data["promotion"]["phonetic_examples_promoted"] == 0
    assert data["promotion"]["cultural_claims_promoted"] == 0
    assert data["promotion"]["evidence_claim_count_change"] is False


def test_run251_search_log_covers_requested_classes():
    p = Path("data/source_census/search_log_run251.jsonl")
    rows = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {r["class"] for r in rows}
    required = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert required.issubset(classes)
    assert {r["search_id"] for r in rows} == {"MMSC-SEARCH-000251"}
