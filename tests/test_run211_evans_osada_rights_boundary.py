import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/evans_osada_2005_repository_rights_boundary_run211_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run211.jsonl"


def test_run211_evans_osada_identity_pagination_and_rights_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    rec = data["record"]
    ver = data["verification"]
    gov = data["rights_access_consent_cultural_governance"]
    assert data["run"] == 211
    assert rec["doi"] == "10.1515/lity.2005.9.3.351"
    assert rec["anu_handle"] == "1885/54663"
    assert rec["bibliographic_pages"] == "351-390"
    assert rec["bibliographic_page_span"] == 40
    assert rec["publisher_and_anu_bibliographic_pagination_agree"] is True
    assert ver["repository_rights_note_verified"] is True
    assert ver["file_bytes_verified"] is False
    assert ver["file_checksum_verified"] is False
    assert ver["file_internal_page_sequence_verified"] is False
    assert ver["linguistic_claim_promoted"] is False
    assert ver["cultural_claim_promoted"] is False
    assert gov["open_access_is_not_blanket_reuse_permission"] is True
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False


def test_run211_census_counts_frozen_and_all_classes_present():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000211"
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
