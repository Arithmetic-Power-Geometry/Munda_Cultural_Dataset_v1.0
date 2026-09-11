import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/evans_osada_2005_anu_exact_page_locator_run218_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run218.jsonl"


def test_run218_evans_osada_exact_locator_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    src = data["source_identity"]
    loc = data["exact_locator"]
    ver = data["verification_boundary"]
    gov = data["rights_governance"]
    assert data["run"] == 218
    assert src["doi"] == "10.1515/lity.2005.9.3.351"
    assert src["anu_handle"] == "1885/54663"
    assert src["pages"] == "351-390"
    assert src["access_statement"] == "Open Access"
    assert loc["article_page"] == 385
    assert loc["indexed_full_text_observed"] is True
    assert loc["page_image_verified_in_this_run"] is False
    assert loc["byte_preserving_download_completed_in_this_run"] is False
    assert loc["independent_checksum_computed"] is False
    assert ver["exact_article_page_locator_verified_from_indexed_repository_text"] is True
    assert ver["linguistic_claim_promoted_to_public_evidence_graph"] is False
    assert ver["cultural_claim_promoted"] is False
    assert ver["source_identity_count_changed"] is False
    assert gov["rights_note_interpreted_as_general_redistribution_license"] is False
    assert gov["model_training_permission_inferred"] is False
    assert gov["participant_consent_inferred"] is False
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False


def test_run218_counts_and_all_class_census_remain_conservative():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000218"
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
