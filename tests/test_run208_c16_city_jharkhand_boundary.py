import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/census_c16_city_jharkhand_catalogue_exact_locator_run208_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run208.jsonl"


def test_run208_c16_city_exact_locator_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    src = data["source"]
    ver = data["verification"]
    assert data["run"] == 208
    assert src["reference_id"] == "PC11_C16city-20"
    assert src["reference_number"] == "PC11_C16city"
    assert src["download_filename_catalogued"] == "DDW-C16-TOWN-STMT-MDDS-2000.XLSX"
    assert "town" in src["geographic_granularity"]
    assert ver["official_catalogue_identity_verified"] is True
    assert ver["workbook_bytes_acquired"] is False
    assert ver["independent_file_hash_verified"] is False
    assert ver["exact_numeric_cells_verified"] is False
    assert ver["numeric_values_promoted"] is False
    assert data["deduplication"]["count_bearing_source_identity_added"] is False
    assert data["evidence_promotion"]["new_cultural_claims"] == 0
    assert data["rights_access_governance"]["participant_consent_inferred"] is False
    assert data["rights_access_governance"]["community_validation_inferred"] is False
    assert data["rights_access_governance"]["cultural_access_permission_inferred"] is False


def test_run208_all_requested_source_classes_logged():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000208"
    assert expected.issubset(set(row["classes"]))
    assert row["counts_changed"] is False
    assert row["cultural_claims_added"] == 0
