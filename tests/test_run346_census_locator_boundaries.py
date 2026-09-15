import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCATOR = ROOT / "data" / "source_census" / "exact_locator_records_run346_2026-09-14.json"
MMSC = ROOT / "audits" / "mmsc_search_run346_2026-09-14.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run346_census_locator_does_not_promote_unverified_cells():
    data = _load(LOCATOR)
    assert data["run"] == 346
    ids = {record["source_id"] for record in data["records"]}
    assert "PC11_C17-20" in ids
    c17 = next(record for record in data["records"] if record["source_id"] == "PC11_C17-20")
    assert c17["declared_download_filename"] == "DDW-C17-2000.XLSX"
    assert c17["content_promoted"] is False
    boundary = data["verification_boundaries"]
    assert boundary["primary_workbook_bytes_verified"] is False
    assert boundary["independent_sha256_verified"] is False
    assert boundary["sheet_inventory_verified"] is False
    assert boundary["row_counts_verified"] is False
    assert boundary["cell_values_verified"] is False
    assert boundary["numeric_claims_promoted"] == 0
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_authorization_inferred"] is False
    assert boundary["cultural_or_linguistic_claims_promoted"] == 0


def test_run346_controlled_counts_remain_stable_without_webmun_disposition():
    data = _load(MMSC)
    assert data["controlled_counts_changed"] is False
    assert data["deduplication"]["numbered_WEB_MUN_dispositions_completed_this_run"] == 0
    counts = data["controlled_counts"]
    assert counts == {
        "audited_source_identities": 42,
        "raw_web_discovery_records": 90,
        "unique_web_discovery_leads": 87,
        "duplicate_web_records": 3,
        "canonicalized_unique_web_leads": 14,
        "unresolved_unique_web_leads": 73,
        "claims": 52,
        "evidence_records": 52,
        "provenance_links": 52,
        "streamlit_modules": 42,
    }
    assert data["governance"]["numeric_claims_promoted"] == 0
    assert data["governance"]["cultural_or_linguistic_claims_promoted"] == 0
