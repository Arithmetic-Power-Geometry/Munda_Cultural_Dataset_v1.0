import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/mundarica_volume_v_manifestation_audit_run213_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run213.jsonl"


def test_run213_volume_v_exact_secondary_manifestation_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    rec = data["record"]
    ver = data["verification"]
    gov = data["rights_access_consent_cultural_governance"]
    assert data["run"] == 213
    assert rec["volume"] == "V"
    assert rec["internet_archive_identifier"] == "in.ernet.dli.2015.14925"
    assert rec["ark"] == "ark:/13960/t1mh2xz66"
    assert rec["catalogued_total_pages"] == 278
    assert rec["pdf_degraded_observed"] == "invalid-jp2-headers"
    assert ver["exact_secondary_manifestation_verified"] is True
    assert ver["catalogued_page_count_verified_from_item_metadata"] is True
    assert ver["authoritative_scan_verified"] is False
    assert ver["independent_file_hash_verified"] is False
    assert ver["scan_sequence_independently_verified"] is False
    assert ver["ocr_verified_as_transcription"] is False
    assert ver["volume_verified_complete"] is False
    assert ver["cultural_claim_promoted"] is False
    assert ver["linguistic_claim_promoted"] is False
    assert ver["passage_level_ingestion_performed"] is False
    assert gov["archive_rights_label_is_not_community_permission"] is True
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False


def test_run213_counts_frozen_and_all_class_census_logged():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000213"
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
    assert row["release_gate"] == "NOT_PASS"
