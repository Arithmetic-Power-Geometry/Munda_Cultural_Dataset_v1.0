import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/census_2011_c16_jharkhand_manifestation_audit_run189_2026-09-11.json"
SEARCH = ROOT / "data/source_census/search_log_run189.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run189_c16_identity_and_verification_boundary():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert a["identity"]["reference_id"] == "PC11_C16-20"
    assert a["identity"]["reference_number"] == "PC11_C16"
    assert a["identity"]["workbook_filename"] == "DDW-C16-STMT-MDDS-2000.xlsx"
    assert a["catalogue_munda_mundari_row_labels_verified"] is True
    labels = {x["catalogue_label"] for x in a["catalogue_row_locators"]}
    assert {"91 MUNDA", "92 MUNDARI"}.issubset(labels)
    assert a["workbook_bytes_acquired"] is False
    assert a["independent_checksum_verified"] is False
    assert a["worksheet_names_verified"] is False
    assert a["workbook_row_numbers_verified"] is False
    assert a["numeric_cells_verified"] is False
    assert a["numeric_values_promoted"] is False
    assert a["canonicalization"]["count_bearing"] is False
    assert a["cultural_governance"]["cultural_claims_promoted"] == 0
    assert a["cultural_governance"]["participant_records_ingested"] == 0
    assert a["cultural_governance"]["community_validation_inferred"] is False
    assert a["cultural_governance"]["participant_consent_inferred"] is False
    assert a["cultural_governance"]["cultural_access_permission_inferred"] is False


def test_run189_all_requested_source_classes_logged():
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


def test_run189_preserves_controlled_counts():
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    assert s["mmsc"]["audited_source_identities"] == 42
    assert s["mmsc"]["raw_web_discovery_records"] == 90
    assert s["mmsc"]["unique_web_discovery_leads"] == 87
    assert s["mmsc"]["duplicate_web_records"] == 3
    assert s["mmsc"]["canonicalized_unique_web_leads"] == 14
    assert s["mmsc"]["unresolved_unique_web_leads"] == 73
    assert s["evidence_and_schema"]["source_claims"] == 52
    assert s["evidence_and_schema"]["evidence_records"] == 52
    assert s["evidence_and_schema"]["evidence_links"] == 52
