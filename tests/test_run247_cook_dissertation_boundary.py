import json
from pathlib import Path


def test_run247_cook_dissertation_audit_boundary():
    p = Path("data/source_census/cook_1965_mundari_dissertation_exact_locator_run247_2026-09-12.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["run_id"] == 247
    assert data["work"]["year"] == 1965
    assert data["work"]["institution"] == "Georgetown University"
    assert data["deduplication"]["canonical_key"] == "cook|1965|a-descriptive-analysis-of-mundari|georgetown-university"
    refs = {x.get("reference_id") for x in data["verified_locators"] if x["provider"] == "Glottolog 5.3"}
    assert {"33106", "152623"}.issubset(refs)
    assert data["rights_access_boundary"]["full_text_bytes_acquired"] is False
    assert data["rights_access_boundary"]["cryptographic_hash_verified"] is False
    assert data["content_evidence_promoted"] is False
    assert data["lexical_rows_promoted"] == 0
    assert data["grammatical_propositions_promoted"] == 0
    assert data["cultural_claims_promoted"] == 0
    assert data["identity_count_change"] is False
    assert data["evidence_claim_count_change"] is False


def test_run247_search_log_covers_requested_classes():
    p = Path("data/source_census/search_log_run247.jsonl")
    rows = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {r["class"] for r in rows}
    required = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert required.issubset(classes)
    assert {r["search_id"] for r in rows} == {"MMSC-SEARCH-000247"}
