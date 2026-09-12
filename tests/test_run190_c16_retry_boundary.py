import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/census_2011_c16_jharkhand_retry_audit_run190_2026-09-11.json"
SEARCH = ROOT / "data/source_census/search_log_run190.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run190_c16_retry_does_not_promote_unverified_workbook_data():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert a["identity"]["reference_id"] == "PC11_C16-20"
    assert a["identity"]["workbook_filename"] == "DDW-C16-STMT-MDDS-2000.xlsx"
    assert a["fresh_search_index_verification"]["official_catalogue_identity_visible"] is True
    assert a["direct_authoritative_page_fetch"]["result"] == "HTTP 502 Bad Gateway"
    assert a["workbook_bytes_acquired"] is False
    assert a["independent_checksum_verified"] is False
    assert a["worksheet_names_verified"] is False
    assert a["workbook_row_numbers_verified"] is False
    assert a["numeric_cells_verified"] is False
    assert a["numeric_values_promoted"] is False
    assert a["count_bearing"] is False
    assert a["claims_added"] == 0
    assert a["evidence_records_added"] == 0
    assert a["evidence_links_added"] == 0
    assert a["participant_records_ingested"] == 0
    assert a["public_availability_treated_as_permission"] is False
    assert a["community_validation_inferred"] is False
    assert a["participant_consent_inferred"] is False
    assert a["cultural_access_permission_inferred"] is False


def test_run190_all_requested_source_classes_logged_without_count_inflation():
    row = json.loads(SEARCH.read_text(encoding="utf-8").strip())
    required = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI materials",
        "archives", "newspapers/periodicals", "web resources", "datasets",
        "audio", "video", "maps", "relevant media",
    }
    assert required.issubset(set(row["source_classes"]))
    assert row["mmsc_count_change"] == 0
    assert row["claim_count_change"] == 0
    assert row["evidence_count_change"] == 0
    assert row["source_identity_count_change"] == 0
    assert row["absolute_or_future_proof_completeness_claimed"] is False


def test_run190_status_preserves_release_gate_and_counts():
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    assert s["latest_run"] >= 190
    assert s["mmsc"]["audited_source_identities"] == 42
    assert s["mmsc"]["unresolved_unique_web_leads"] == 73
    assert s["evidence_and_schema"]["source_claims"] == 52
    assert s["evidence_and_schema"]["evidence_records"] == 52
    assert s["evidence_and_schema"]["evidence_links"] == 52
    assert s["release_gate"]["status"] == "NOT_PASS"
    assert s["release_gate"]["automated_completeness_audit_pass"] is False
