import json
from pathlib import Path


def test_run252_ciil_catalogue_boundary():
    p = Path("data/source_census/sinha_1974_mundari_phonetic_reader_ciil_catalogue_run252_2026-09-12.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["run_id"] == 252
    assert data["work"]["canonical_title"] == "Mundari Phonetic Reader"
    assert data["work"]["author"] == "N. K. Sinha"
    assert data["work"]["year"] == 1974
    assert data["work"]["series_number"] == 13
    obs = data["official_ciil_catalogue_observation"]
    assert obs["provider"] == "Central Institute of Indian Languages (CIIL)"
    assert obs["pages"] == 102
    assert obs["content_language"] == "English"
    assert obs["subject_language"] == "Mundari"
    assert "catalogue metadata" in obs["verification_level"]
    assert data["deduplication"]["canonical_key"] == "sinha-nk|1974|mundari-phonetic-reader|ciil-series-13"
    assert data["deduplication"]["identity_count_change"] is False
    assert len(data["cross_source_extent_conflict"]["observations"]) >= 6
    boundary = data["rights_access_boundary"]
    assert boundary["full_text_bytes_acquired"] is False
    assert boundary["cryptographic_hash_verified"] is False
    assert boundary["scan_sequence_to_printed_pagination_verified"] is False
    assert boundary["ocr_verified"] is False
    assert boundary["redistribution_permission_verified"] is False
    assert boundary["community_validation_verified"] is False
    assert boundary["cultural_access_permission_verified"] is False
    assert boundary["cultural_access_overrides_entitlement"] is True
    promotion = data["promotion"]
    assert promotion["content_evidence_promoted"] is False
    assert promotion["passages_promoted"] == 0
    assert promotion["phonetic_examples_promoted"] == 0
    assert promotion["linguistic_claims_promoted"] == 0
    assert promotion["cultural_claims_promoted"] == 0
    assert promotion["evidence_claim_count_change"] is False


def test_run252_search_log_covers_requested_classes():
    p = Path("data/source_census/search_log_run252.jsonl")
    rows = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {r["class"] for r in rows}
    required = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert required.issubset(classes)
    assert {r["search_id"] for r in rows} == {"MMSC-SEARCH-000252"}
