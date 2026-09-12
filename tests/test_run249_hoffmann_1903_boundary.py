import json
from pathlib import Path


def test_run249_hoffmann_1903_audit_boundary():
    p = Path("data/source_census/hoffmann_1903_mundari_grammar_exact_locator_run249_2026-09-12.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["run_id"] == 249
    assert data["work"]["year"] == 1903
    assert data["work"]["publisher"] == "Bengal Secretariat Press"
    assert data["work"]["extent_google_books"] == "222 pages"
    assert data["deduplication"]["canonical_key"] == "hoffmann|1903|mundari-grammar|bengal-secretariat-press"
    ids = {x["book_id"] for x in data["verified_locators"] if x["provider"] == "Google Books"}
    assert {"V9cj0AEACAAJ", "KfIitwAACAAJ"}.issubset(ids)
    assert data["rights_access_boundary"]["full_text_bytes_acquired"] is False
    assert data["rights_access_boundary"]["cryptographic_hash_verified"] is False
    assert data["rights_access_boundary"]["page_image_sequence_verified"] is False
    assert data["rights_access_boundary"]["ocr_verified"] is False
    assert data["content_evidence_promoted"] is False
    assert data["lexical_rows_promoted"] == 0
    assert data["grammatical_propositions_promoted"] == 0
    assert data["cultural_claims_promoted"] == 0
    assert data["identity_count_change"] is False
    assert data["evidence_claim_count_change"] is False


def test_run249_search_log_covers_requested_classes():
    p = Path("data/source_census/search_log_run249.jsonl")
    rows = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {r["class"] for r in rows}
    required = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert required.issubset(classes)
    assert {r["search_id"] for r in rows} == {"MMSC-SEARCH-000249"}
