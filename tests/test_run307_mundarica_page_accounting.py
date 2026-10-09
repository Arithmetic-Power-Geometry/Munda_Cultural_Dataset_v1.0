import json
from pathlib import Path

AUDIT = Path("data/source_census/mundarica_google_books_page_accounting_run307_2026-09-13.json")
LOG = Path("data/source_census/search_log_run307.jsonl")


def test_run307_mundarica_page_accounting_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["run_id"] == 307
    assert [m["logical_volume"] for m in data["manifestations"]] == ["VIII", "XI"]
    assert data["manifestations"][0]["visible_contents_printed_page_anchors"] == [2147, 2151, 2208]
    assert data["manifestations"][1]["visible_contents_printed_page_anchors"] == [3173, 3175, 3183]
    effect = data["page_accounting_effect"]
    assert effect["historical_printed_page_anchors_added"] == 6
    assert effect["authoritative_registered_scans_added"] == 0
    assert effect["verified_complete_volumes_added"] == 0
    assert effect["ocr_pages_verified_added"] == 0
    boundary = data["verification_boundary"]
    assert boundary["source_bytes_acquired_and_hashed"] is False
    assert boundary["page_images_independently_verified"] is False
    assert boundary["printed_page_to_scan_image_concordance_verified"] is False
    assert boundary["ocr_independently_verified"] is False
    assert boundary["rights_for_bulk_reuse_verified"] is False
    assert boundary["community_validation_verified"] is False
    assert boundary["cultural_access_permission_verified"] is False
    assert data["promotion"]["new_controlled_cultural_claims"] == 0
    assert data["promotion"]["new_controlled_evidence_records"] == 0
    assert data["promotion"]["count_bearing_change"] is False


def test_run307_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI materials", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio", "video",
        "maps", "relevant media"
    }
    assert {row["class"] for row in rows} == expected
    books = next(row for row in rows if row["class"] == "books")
    assert books["result"] == "promoted-page-accounting-locator"
    assert "vAWmtdk21wEC" in books["source"]
