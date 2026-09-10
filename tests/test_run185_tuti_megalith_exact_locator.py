import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/tuti_et_al_2025_munda_megaliths_exact_locator_run185_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run185.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run185_source_identity_and_exact_locator_boundary():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["run"] == 185
    assert d["branch"] == "mlhkp-v2"
    assert d["source"]["doi"] == "10.30884/seh/2025.02.01"
    assert d["source"]["publication_month"] == "September 2025"
    assert d["source"]["peer_reviewed_article"] is True
    assert d["release_effect"]["discovery_only"] is False
    assert d["release_effect"]["exact_locator_level_reached"] is True
    assert len(d["exact_locators"]) >= 4


def test_run185_rights_consent_and_cultural_access_not_overclaimed():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    g = d["rights_access_consent_cultural_uncertainty"]
    assert g["publisher_full_html_access_observed"] is True
    assert g["article_license_value_verified"] is False
    assert g["reuse_permission_inferred_from_public_access"] is False
    assert g["study_verbal_consent_reported_by_authors"] is True
    assert g["study_consent_treated_as_mlkhp_secondary_reuse_consent"] is False
    assert g["participant_level_content_ingested"] is False
    assert g["sensitive_cultural_content_ingested"] is False
    assert g["community_validation_inferred"] is False
    assert g["cultural_access_permission_inferred"] is False
    assert d["evidence_boundary"]["cultural_claims_added_run185"] == 0
    assert d["evidence_boundary"]["participant_records_added_run185"] == 0
    assert d["evidence_boundary"]["count_bearing_change"] is False


def test_run185_census_has_all_release_classes():
    rows = [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 12
    assert {r["search_id"] for r in rows} == {"MMSC-SEARCH-000185"}
    assert {r["class"] for r in rows} == {
        "books_dictionaries_grammars", "peer_reviewed_articles", "theses_dissertations",
        "government_tri_census_lsi", "archives", "newspapers_periodicals", "web_resources",
        "datasets", "audio", "video", "maps", "relevant_media"
    }


def test_run185_status_and_count_contract():
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    assert s["latest_run"] >= 185
    assert s["branch"] == "mlhkp-v2"
    assert s["mmsc"]["audited_source_identities"] == 42
    assert s["mmsc"]["raw_web_discovery_records"] == 90
    assert s["mmsc"]["unique_web_discovery_leads"] == 87
    assert s["mmsc"]["duplicate_web_records"] == 3
    assert s["mmsc"]["canonicalized_unique_web_leads"] == 14
    assert s["mmsc"]["unresolved_unique_web_leads"] == 73
    assert s["evidence_and_schema"]["source_claims"] == 52
    assert s["evidence_and_schema"]["evidence_records"] == 52
    assert s["evidence_and_schema"]["evidence_links"] == 52
    assert s["streamlit"]["registered_modules"] == 42
    assert s["streamlit"]["mapped_modules"] == 42
    assert s["release_gate"]["status"] == "NOT_PASS"
