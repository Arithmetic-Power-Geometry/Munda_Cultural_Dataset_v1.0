import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lsi_jharkhand_mirror_corroboration_run217_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run217.jsonl"


def test_run217_lsi_mirror_corroboration_does_not_overclaim():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    mirror = data["independent_readable_copy"]
    ver = data["verification_boundary"]
    gov = data["rights_governance"]
    assert data["run"] == 217
    assert data["official_identity"]["reference_id"] == "LSI_JHARKHAND"
    assert data["official_identity"]["official_filename"] == "LSI_JHARKHAND.pdf"
    assert mirror["indexed_page_marker"] == 71
    assert mirror["indexed_text_contains_mundari_section"] is True
    assert mirror["binary_download_completed_in_this_run"] is False
    assert mirror["page_image_screenshot_verified_in_this_run"] is False
    assert mirror["independent_checksum_computed"] is False
    assert ver["independent_host_textual_corroboration_verified"] is True
    assert ver["official_and_mirror_bytes_proven_identical"] is False
    assert ver["official_pdf_bytes_acquired_byte_preservingly"] is False
    assert ver["exact_numeric_values_promoted_to_public_evidence"] is False
    assert ver["linguistic_proposition_promoted"] is False
    assert ver["cultural_proposition_promoted"] is False
    assert gov["public_access_is_not_reuse_permission"] is True
    assert gov["mirror_access_does_not_override_official_rights"] is True
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False


def test_run217_counts_and_all_class_census_remain_conservative():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000217"
    assert expected.issubset(set(row["classes"]))
    assert row["counts_changed"] is False
    assert row["audited_source_identities"] == 42
    assert row["raw_web_discovery_records"] == 90
    assert row["unique_web_discovery_leads"] == 87
    assert row["duplicate_web_records"] == 3
    assert row["canonicalized_unique_web_leads"] == 14
    assert row["unresolved_unique_web_leads"] == 73
    assert row["source_claims"] == 52
    assert row["evidence_records"] == 52
    assert row["evidence_links"] == 52
    assert row["streamlit_modules"] == 42
    assert row["cultural_claims_added"] == 0
    assert row["linguistic_claims_added"] == 0
    assert row["release_gate"] == "NOT_PASS"
