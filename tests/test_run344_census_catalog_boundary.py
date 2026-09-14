import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCATOR = ROOT / "data" / "source_census" / "census_c16_st16_schema_locator_run344_2026-09-14.json"
MMSC = ROOT / "audits" / "mmsc_search_run344_2026-09-14.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run344_census_catalogue_metadata_cannot_be_promoted_as_cell_verification():
    data = _load(LOCATOR)
    boundary = data["verification_boundaries"]
    assert data["run"] == 344
    assert len(data["sources"]) == 2
    assert {s["source_id"] for s in data["sources"]} == {"PC11_C16-20", "PC11_ST16-20"}
    assert all(s["verification_level"] == "official_catalogue_metadata_only" for s in data["sources"])
    assert boundary["primary_workbook_bytes_verified"] is False
    assert boundary["independent_sha256_verified"] is False
    assert boundary["sheet_inventory_verified"] is False
    assert boundary["row_count_verified"] is False
    assert boundary["cell_values_verified"] is False
    assert boundary["mundari_specific_numeric_values_verified"] is False
    assert boundary["numeric_claims_promoted"] == 0
    assert boundary["cultural_or_linguistic_claims_promoted"] == 0
    assert boundary["rights_or_cultural_access_inferred_from_catalogue_availability"] is False


def test_run344_mmsc_counts_stay_controlled_without_numbered_reconciliation():
    data = _load(MMSC)
    counts = data["controlled_counts"]
    assert data["controlled_counts_changed"] is False
    assert data["deduplication"]["numbered_WEB_MUN_dispositions_completed_this_run"] == 0
    assert counts == {
        "audited_source_identities": 42,
        "raw_web_discovery_records": 90,
        "unique_web_discovery_leads": 87,
        "duplicate_web_records": 3,
        "canonicalized_unique_web_leads": 14,
        "unresolved_unique_web_leads": 73,
    }
    assert data["governance"]["numeric_claims_promoted"] == 0
    assert data["governance"]["cultural_or_linguistic_claims_promoted"] == 0
