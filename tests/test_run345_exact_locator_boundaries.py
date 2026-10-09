import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCATOR = ROOT / "data" / "source_census" / "exact_locator_records_run345_2026-09-14.json"
MMSC = ROOT / "audits" / "mmsc_search_run345_2026-09-14.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run345_exact_locators_do_not_become_unverified_content():
    data = _load(LOCATOR)
    assert data["run"] == 345
    assert {r["source_id"] for r in data["records"]} == {
        "PC11_C16city-20",
        "PC11_ST15-20",
        "BHARATAVANI-MUNDARI-DICTIONARIES",
    }
    assert all(r["content_promoted"] is False for r in data["records"] if "content_promoted" in r)
    boundary = data["verification_boundaries"]
    assert boundary["census_primary_workbook_bytes_verified"] is False
    assert boundary["census_independent_sha256_verified"] is False
    assert boundary["census_sheet_row_cell_values_verified"] is False
    assert boundary["census_numeric_claims_promoted"] == 0
    assert boundary["bharatavani_pdf_bytes_verified"] is False
    assert boundary["bharatavani_entry_content_verified"] is False
    assert boundary["bharatavani_reuse_permission_established"] is False
    assert boundary["participant_consent_inferred"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_authorization_inferred"] is False
    assert boundary["linguistic_or_cultural_claims_promoted"] == 0


def test_run345_controlled_counts_stay_frozen_without_numbered_webmun_disposition():
    data = _load(MMSC)
    assert data["controlled_counts_changed"] is False
    assert data["deduplication"]["numbered_WEB_MUN_dispositions_completed_this_run"] == 0
    counts = data["controlled_counts"]
    assert counts["audited_source_identities"] == 42
    assert counts["raw_web_discovery_records"] == 90
    assert counts["unique_web_discovery_leads"] == 87
    assert counts["duplicate_web_records"] == 3
    assert counts["canonicalized_unique_web_leads"] == 14
    assert counts["unresolved_unique_web_leads"] == 73
    assert counts["claims"] == 52
    assert counts["evidence_records"] == 52
    assert counts["provenance_links"] == 52
    assert counts["streamlit_modules"] == 42
    assert data["governance"]["numeric_claims_promoted"] == 0
    assert data["governance"]["cultural_or_linguistic_claims_promoted"] == 0
