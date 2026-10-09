import json
from pathlib import Path

AUDIT = Path("data/source_census/dilbar_hans_mundari_hockey_rulebook_locator_run288_2026-09-13.json")
SEARCH = Path("data/source_census/search_log_run288.jsonl")


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_secondary_locator_is_precise_but_not_primary_promotion():
    data = load_audit()
    assert data["run_id"] == 288
    assert data["scope_classification"]["not_mundarica"] is True
    assert data["secondary_source"]["publisher"] == "The Indian Express"
    assert data["secondary_source"]["published_date"] == "2023-10-18"
    assert data["reported_primary_item"]["first_publication_year_reported"] == 1941
    assert data["reported_primary_item"]["extent_pages_reported"] == 23
    assert data["reported_primary_item"]["primary_copy_or_scan_obtained"] is False
    assert data["reported_primary_item"]["primary_bytes_hashed"] is False
    assert data["reported_primary_item"]["page_image_concordance_verified"] is False
    assert data["reported_primary_item"]["ocr_or_transcription_verified"] is False
    assert data["scope_classification"]["cultural_claim_promotion"] is False


def test_rights_and_governance_boundaries_remain_closed():
    data = load_audit()
    boundary = data["rights_access_consent_cultural_boundary"]
    assert boundary["newspaper_public_access_treated_as_primary_book_permission"] is False
    assert boundary["private_copy_report_treated_as_redistribution_permission"] is False
    assert boundary["primary_item_public_domain_assumed"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_permission_inferred"] is False
    assert boundary["controlled_claim_rows_added"] == 0
    assert boundary["controlled_evidence_rows_added"] == 0
    assert boundary["controlled_evidence_links_added"] == 0
    assert boundary["primary_text_or_images_ingested"] == 0


def test_search_log_covers_all_fourteen_controlled_classes():
    records = [json.loads(line) for line in SEARCH.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert len(records) == 14
    assert {r["class"] for r in records} == expected
    assert all(r["run_id"] == 288 for r in records)
