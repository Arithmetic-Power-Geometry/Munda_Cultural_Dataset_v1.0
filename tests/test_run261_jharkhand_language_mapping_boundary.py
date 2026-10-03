import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "jharkhand_language_mapping_phase1_mundari_exact_locator_run261_2026-09-12.json"
LOG = ROOT / "data" / "source_census" / "search_log_run261.jsonl"


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run261_exact_report_identity_and_locators():
    d = load_audit()
    assert d["run_id"] == 261
    src = d["source"]
    assert src["title"].startswith("Language Mapping of Schools in Jharkhand")
    assert src["document_pages"] == 48
    assert src["survey_data_collection_period"] == "January-February 2024"
    locators = {x["locator"] for x in d["exact_locators"]}
    assert any("p.19" in x and "Table 1" in x for x in locators)
    assert any("p.24" in x and "Table 2" in x for x in locators)
    assert any("p.31" in x and "Table 4" in x for x in locators)


def test_run261_mundari_aggregate_values_are_scope_bounded():
    d = load_audit()
    joined = " ".join(x["supported_metadata_or_scope"] for x in d["exact_locators"])
    assert "7.32%" in joined
    assert "393 schools" in joined
    assert "145 teachers" in joined
    assert "366" in joined
    boundaries = " ".join(x["promotion_boundary"] for x in d["exact_locators"])
    assert "not a Census population estimate" in boundaries
    assert "no individual-level or cultural inference" in boundaries


def test_run261_rights_consent_and_content_boundaries_hold():
    d = load_audit()
    b = d["rights_access_consent_cultural_boundary"]
    p = d["promotion"]
    assert b["direct_pdf_publicly_accessible"] is True
    assert b["explicit_redistribution_license_verified"] is False
    assert b["model_training_permission_verified"] is False
    assert b["individual_student_or_teacher_records_ingested"] is False
    assert b["participant_consent_independently_verified"] is False
    assert b["community_validation_verified"] is False
    assert b["cultural_access_permission_verified"] is False
    assert p["discovery_only"] is False
    assert p["exact_locator_records_promoted"] == 5
    assert p["controlled_claim_rows_added"] == 0
    assert p["controlled_evidence_rows_added"] == 0
    assert p["controlled_evidence_links_added"] == 0
    assert p["cultural_claims_promoted"] == 0
    assert p["participant_derived_records_promoted"] == 0


def test_run261_dedup_and_screenshot_failure_are_explicit():
    d = load_audit()
    dedup = d["deduplication"]
    assert dedup["identity_count_change"] is False
    assert dedup["canonical_key"].startswith("url:https://languageandlearningfoundation.org/")
    assert len(d["blocked_attempts"]) == 1
    assert "screenshot" in d["blocked_attempts"][0]["source"].lower()
    assert "do not claim image-level verification" in d["blocked_attempts"][0]["disposition"]


def test_run261_search_log_covers_all_required_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {row["class"] for row in rows}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert classes == expected
    assert len(rows) == 14
    assert all(row["search_id"] == "MMSC-SEARCH-000261" for row in rows)
