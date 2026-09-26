import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/visva_bharati_mundari_bibliography_audit_run215_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run215.jsonl"
COVERAGE = ROOT / "data/coverage_matrix.json"


def test_run215_visva_bharati_mundari_bibliography_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    rec = data["record"]
    sec = data["mundari_section"]
    mund = data["mundarica_reconciliation"]
    ver = data["verification"]
    gov = data["rights_access_consent_cultural_governance"]
    assert data["run"] == 215
    assert rec["year"] == 2022
    assert rec["isbn"] == "978-81-957226-2-4"
    assert rec["pdf_pages_observed_by_retrieval"] == 435
    assert sec["section_heading_directly_observed"] is True
    assert sec["section_starts_pdf_page_index"] == 298
    assert sec["section_printed_page"] == 299
    assert {"Research", "Book", "Dictionary"}.issubset(set(sec["observed_categories"]))
    assert mund["conflicting_volume_descriptions_present"] is True
    assert "Volume-1-13" in mund["citation_a_directly_observed"]
    assert "Volume-1-16" in mund["citation_b_directly_observed"]
    assert mund["canonical_volume_count_resolved_by_this_source"] is False
    assert mund["authoritative_scan_verified"] is False
    assert mund["verified_complete_volume_verified"] is False
    assert mund["new_mundarica_volume_state_promoted"] is False
    assert ver["institutional_pdf_text_manifestation_verified"] is True
    assert ver["pdf_bytes_independently_hashed"] is False
    assert ver["cultural_claim_promoted"] is False
    assert ver["linguistic_claim_promoted"] is False
    assert gov["open_license_inferred"] is False
    assert gov["bibliographic_listing_is_not_reuse_permission"] is True
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False


def test_run215_counts_frozen_all_classes_and_coverage_contract_present():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000215"
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
    assert rows["COV-008"]["gap_rule"] == "consent and rights required before public exposure"
    assert "never claim absolute completeness" in rows["COV-025"]["gap_rule"]
