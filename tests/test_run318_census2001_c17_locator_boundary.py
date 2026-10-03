import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "census_2001_c17_jharkhand_locator_run318_2026-09-14.json"
STATUS = ROOT / "status" / "mlhkp_progress.json"
SEARCH_LOG = ROOT / "data" / "source_census" / "search_log_run318.jsonl"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_census2001_c17_exact_locator_and_boundary():
    audit = load_json(AUDIT)
    assert audit["run"] == 318
    assert audit["reference_id"] == "PC01_C17-20"
    assert audit["declared_download"] == "PC01_C17_20.xls"
    assert audit["authority"] == "Office of the Registrar General & Census Commissioner, India"

    verification = audit["verification"]
    assert verification["catalogue_identity_verified"] is True
    assert verification["declared_workbook_filename_verified"] is True
    assert verification["workbook_bytes_acquired"] is False
    assert verification["independent_hash_verified"] is False
    assert verification["sheet_inventory_verified"] is False
    assert verification["munda_mundari_exact_rows_verified_from_workbook"] is False
    assert verification["exact_numeric_cells_verified"] is False

    promotion = audit["promotion"]
    assert promotion["catalogue_locator_promoted"] is True
    assert promotion["numeric_claims_promoted"] == 0
    assert promotion["linguistic_claims_promoted"] == 0
    assert promotion["cultural_claims_promoted"] == 0
    assert promotion["controlled_source_count_increment"] == 0
    assert promotion["controlled_evidence_record_increment"] == 0
    assert promotion["controlled_provenance_link_increment"] == 0

    governance = audit["rights_governance"]
    assert governance["workbook_reuse_permission_not_inferred"] is True
    assert governance["participant_consent_not_inferred"] is True
    assert governance["community_validation_not_inferred"] is True
    assert governance["cultural_authorization_not_inferred"] is True

    scope = audit["scope_disambiguation"]
    assert scope["south_sudan_mundari_false_positive_excluded"] is True


def test_run318_fourteen_class_log_and_count_neutral_status():
    rows = [json.loads(line) for line in SEARCH_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert {row["source_class"] for row in rows} == {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers", "web resources", "datasets", "audio", "video",
        "maps", "relevant media"
    }

    status = load_json(STATUS)
    assert status["branch"] == "mlhkp-v2"
    assert status["latest_run"] == 318
    assert status["mmsc"]["audited_source_identities"] == 42
    assert status["mmsc"]["raw_web_discovery_records"] == 90
    assert status["mmsc"]["unique_web_discovery_leads"] == 87
    assert status["mmsc"]["duplicate_web_records"] == 3
    assert status["mmsc"]["canonicalized_unique_web_leads"] == 14
    assert status["mmsc"]["unresolved_unique_web_leads"] == 73
    assert status["mmsc"]["latest_search_id"] == "MMSC-SEARCH-000318"
    assert status["mmsc"]["controlled_classes_refreshed_this_run"] == 14
    assert status["evidence"]["claims"] == 52
    assert status["evidence"]["records"] == 52
    assert status["evidence"]["links"] == 52
    assert status["streamlit"]["registered_modules"] == 42
    assert status["streamlit"]["mapped_modules"] == 42
    assert status["release_gate"]["status"] == "NOT_PASS"
    assert status["release_gate"]["automated_completeness_audit_pass"] is False
