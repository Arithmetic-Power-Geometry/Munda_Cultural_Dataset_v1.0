import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/rau_proto_munda_exact_row_locator_run214_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run214.jsonl"
COVERAGE = ROOT / "data/coverage_matrix.json"


def test_run214_rau_exact_row_locator_and_rights_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    rec = data["record"]
    loc = data["exact_locator_verification"]
    recon = data["deterministic_reconciliation"]
    ver = data["verification"]
    gov = data["rights_access_consent_cultural_governance"]
    assert data["run"] == 214
    assert rec["doi"] == "10.5281/zenodo.3380874"
    assert rec["file"] == "pMunda_cognate_set_2019-08-29.csv"
    assert rec["upstream_md5"] == "07e1d945a0fc6cafc4fc7afd3f1ff144"
    assert loc["mundari_columns_directly_observed"] == ["mu_form", "mu_source"]
    assert loc["first_record_id"] == "#A0001"
    assert loc["first_record_gloss"] == "water"
    assert loc["first_record_mundari_form"] == "da:"
    assert loc["first_record_mundari_source_locator"] == "BMED.p31"
    assert loc["last_record_id"] == "#A0127"
    assert loc["last_record_gloss"] == "dirt"
    assert loc["last_record_mundari_form"] == "humu"
    assert loc["last_record_mundari_source_locator"] == "BMED.p73"
    assert recon["same_source_as_existing_rau_lead"] is True
    assert recon["new_source_identity_created"] is False
    assert recon["BMED_p31_underlying_source_page_directly_verified"] is False
    assert ver["direct_file_text_manifestation_verified"] is True
    assert ver["independent_md5_recomputed_from_acquired_bytes"] is False
    assert ver["byte_preserving_local_acquisition_verified"] is False
    assert ver["underlying_BMED_pages_verified"] is False
    assert ver["lexical_claim_promoted"] is False
    assert ver["cultural_claim_promoted"] is False
    assert gov["explicit_license_text_observed_on_record"] is False
    assert gov["open_access_is_not_assumed_to_equal_redistribution_or_training_permission"] is True
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False
    assert gov["row_level_content_redistributed_into_release"] is False


def test_run214_counts_frozen_all_classes_and_coverage_contract_present():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000214"
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
    assert row["exact_locator_records_advanced"] == 1
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    assert coverage["sync_contract"] == "DATA TYPE↔SCHEMA↔SOURCE↔EVIDENCE↔STREAMLIT MODULE↔COVERAGE↔GAP"
    rows = {r["coverage_id"]: r for r in coverage["rows"]}
    assert rows["COV-008"]["gap_rule"] == "consent and rights required before public exposure"
    assert "never claim absolute completeness" in rows["COV-025"]["gap_rule"]
