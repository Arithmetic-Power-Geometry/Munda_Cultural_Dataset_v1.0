import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lsi_jharkhand_official_mundari_locator_run216_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run216.jsonl"
COVERAGE = ROOT / "data/coverage_matrix.json"


def test_run216_official_lsi_jharkhand_mundari_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    rec = data["record"]
    loc = data["mundari_exact_locator"]
    ver = data["verification"]
    gov = data["rights_access_consent_cultural_governance"]
    assert data["run"] == 216
    assert rec["reference_id"] == "LSI_JHARKHAND"
    assert rec["official_filename"] == "LSI_JHARKHAND.pdf"
    assert rec["year"] == 2023
    assert loc["official_pdf_indexed_text_verified"] is True
    assert loc["indexed_pdf_page_marker"] == 71
    assert loc["visual_page_screenshot_verified"] is False
    assert loc["numeric_values_promoted_to_public_evidence"] is False
    assert loc["linguistic_proposition_promoted"] is False
    assert loc["cultural_proposition_promoted"] is False
    assert ver["official_catalogue_identity_verified"] is True
    assert ver["official_download_filename_verified"] is True
    assert ver["official_pdf_bytes_acquired_byte_preservingly"] is False
    assert ver["independent_file_hash_verified"] is False
    assert ver["exact_indexed_text_locator_advanced"] is True
    assert gov["open_license_observed"] is False
    assert gov["public_download_is_not_reuse_permission"] is True
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False


def test_run216_counts_all_classes_and_completeness_contract():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000216"
    assert expected.issubset(set(row["classes"]))
    assert row["counts_changed"] is False
    assert row["audited_source_identities"] == 42
    assert row["unresolved_unique_web_leads"] == 73
    assert row["source_claims"] == 52
    assert row["evidence_records"] == 52
    assert row["evidence_links"] == 52
    assert row["streamlit_modules"] == 42
    assert row["cultural_claims_added"] == 0
    assert row["linguistic_claims_added"] == 0
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    assert coverage["sync_contract"] == "DATA TYPE↔SCHEMA↔SOURCE↔EVIDENCE↔STREAMLIT MODULE↔COVERAGE↔GAP"
    rows = {r["coverage_id"]: r for r in coverage["rows"]}
    assert rows["COV-022"]["coverage_state"] == "live_partial"
    assert "public availability does not imply" in rows["COV-022"]["gap_rule"]
    assert "never claim absolute completeness" in rows["COV-025"]["gap_rule"]
