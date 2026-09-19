import json
from pathlib import Path


def test_run175_c17_manifestation_retry_boundary():
    p = Path("data/source_census/census_2011_c17_jharkhand_manifestation_retry_run175_2026-09-10.json")
    audit = json.loads(p.read_text(encoding="utf-8"))
    assert audit["run"] == 175
    assert audit["source"]["reference_id"] == "PC11_C17-20"
    assert audit["source"]["download_filename"] == "DDW-C17-2000.XLSX"
    assert audit["verification"]["workbook_bytes_acquired"] is False
    assert audit["verification"]["independent_checksum_computed"] is False
    assert audit["verification"]["exact_cell_locators_verified"] is False
    assert audit["evidence_promotion"]["population_values_promoted"] == 0
    assert audit["evidence_promotion"]["cultural_claims_promoted"] == 0
    assert audit["rights_access_boundary"]["redistribution_permission_inferred"] is False
    assert audit["dedupe"]["new_source_identity"] is False
    assert audit["dedupe"]["count_change"] == 0


def test_run175_search_log_covers_requested_classes():
    p = Path("data/source_census/search_log_run175.jsonl")
    row = json.loads(p.read_text(encoding="utf-8"))
    expected = {"books", "dictionaries", "grammars", "peer_reviewed_articles", "theses_dissertations", "government_TRI_Census_LSI", "archives", "newspapers_periodicals", "web_resources", "datasets", "audio", "video", "maps", "relevant_media"}
    assert expected.issubset(set(row["classes"]))
    assert row["count_change"] == 0
    assert row["cultural_claims_added"] == 0
