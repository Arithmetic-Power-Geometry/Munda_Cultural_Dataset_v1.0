import json
from pathlib import Path


def test_run254_mundarica_vii_viii_manifestation_boundaries():
    p = Path("data/source_census/mundarica_vol7_vol8_google_books_manifestation_run254_2026-09-12.json")
    d = json.loads(p.read_text(encoding="utf-8"))

    assert d["run_id"] == 254
    assert d["volumes"] == ["VII", "VIII"]
    providers = {x["volume"]: x for x in d["verified_locators"]}
    assert providers["VII"]["book_id"] == "AUGY0QEACAAJ"
    assert providers["VII"]["displayed_length_pages"] == 265
    assert providers["VIII"]["book_id"] == "vAWmtdk21wEC"
    assert providers["VIII"]["directly_exposed_contents_anchors"] == [2147, 2151, 2208]

    page = d["page_accounting_interpretation"]
    assert page["volume_vii_265_pages_is_catalogue_length_not_scan_image_count"] is True
    assert page["volume_viii_contents_anchors_are_printed_structure_evidence_not_completeness"] is True
    assert page["scan_sequence_verified"] is False
    assert page["printed_page_to_scan_image_reconciliation_complete"] is False

    dedup = d["deduplication"]
    assert dedup["new_source_identity"] is False
    assert dedup["identity_count_change"] is False

    boundary = d["rights_access_cultural_boundary"]
    assert boundary["catalogue_or_snippet_visibility_is_permission"] is False
    assert boundary["full_text_bytes_acquired"] is False
    assert boundary["cryptographic_hash_verified"] is False
    assert boundary["ocr_verified"] is False
    assert boundary["redistribution_permission_inferred"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_permission_inferred"] is False

    promotion = d["promotion"]
    assert promotion["passages_promoted"] == 0
    assert promotion["claims_promoted"] == 0
    assert promotion["content_evidence_promoted"] is False
    assert promotion["count_bearing_change"] is False


def test_run254_all_requested_search_classes_logged():
    rows = [
        json.loads(line)
        for line in Path("data/source_census/search_log_run254.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    classes = {r["class"] for r in rows}
    expected = {
        "books",
        "dictionaries",
        "grammars",
        "peer_reviewed_articles",
        "theses_dissertations",
        "government_TRI_Census_LSI",
        "archives",
        "newspapers_periodicals",
        "web_resources",
        "datasets",
        "audio",
        "video",
        "maps",
        "relevant_media",
    }
    assert expected <= classes
    assert all(r["search_id"] == "MMSC-SEARCH-000254" for r in rows)
