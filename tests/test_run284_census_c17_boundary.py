import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/census_c17_jharkhand_exact_variable_locator_run284_2026-09-13.json"
SEARCH = ROOT / "data/source_census/search_log_run284.jsonl"


def test_run284_c17_exact_variable_locators_and_boundaries():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["source"]["reference_id"] == "PC11_C17-20"
    assert data["source"]["download_filename_declared"] == "DDW-C17-2000.XLSX"
    assert set(data["verified_exact_variable_locators"]) == {
        "Language - Total speakers - MUNDA",
        "Language - Total speakers - MUNDARI",
        "1st subsidiary language - MUNDA",
        "1st subsidiary language - MUNDARI",
        "2nd subsidiary language - MUNDA",
        "2nd subsidiary language - MUNDARI",
    }
    verification = data["verification"]
    assert verification["first_party_catalogue_verified"] is True
    assert verification["declared_workbook_filename_verified"] is True
    assert verification["munda_mundari_variable_names_verified"] is True
    assert verification["workbook_bytes_acquired_this_run"] is False
    assert verification["independent_workbook_hash_verified_this_run"] is False
    assert verification["exact_workbook_cells_verified_this_run"] is False
    assert verification["numeric_values_promoted_this_run"] is False
    promotion = data["promotion"]
    assert promotion["controlled_claims_added"] == 0
    assert promotion["controlled_evidence_records_added"] == 0
    assert promotion["controlled_evidence_links_added"] == 0
    assert promotion["cultural_claims_promoted"] == 0


def test_run284_search_log_covers_all_required_classes():
    records = [json.loads(line) for line in SEARCH.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {r["class"] for r in records}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert classes == expected
    assert len(records) == 14
