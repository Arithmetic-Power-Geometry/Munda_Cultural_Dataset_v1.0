import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/mmloso_2025_mundari_mt_exact_locator_run173_2026-09-10.json"
LOG = ROOT / "data/source_census/search_log_run173.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run173_mmloso_exact_locator_and_rights_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["source_identity"]["anthology_id"] == "2025.mmloso-1.14"
    assert data["source_identity"]["pages"] == "121-129"
    locators = data["exact_locators"]
    assert {x["printed_page"] for x in locators} >= {121, 122, 123}
    assert data["rights_access_consent_cultural_boundary"]["paper_reported_dataset_license"] == "CC BY-SA 4.0"
    assert data["rights_access_consent_cultural_boundary"]["raw_parallel_rows_ingested"] is False
    assert data["rights_access_consent_cultural_boundary"]["participant_consent_verified_for_mlhkp_secondary_use"] is False
    assert data["rights_access_consent_cultural_boundary"]["community_validation_verified"] is False
    assert data["rights_access_consent_cultural_boundary"]["cultural_access_clearance_verified"] is False
    assert data["rights_access_consent_cultural_boundary"]["cultural_claims_promoted"] is False
    assert data["promotion_decision"]["new_permanent_source_identity"] is False
    assert data["promotion_decision"]["new_claim_nodes"] == 0
    notes = " ".join(data["internal_consistency_notes"])
    assert "16,000" in notes and "15,999" in notes


def test_run173_search_classes_and_count_stability():
    records = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    required = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles", "theses_dissertations",
        "government_TRI_Census_LSI", "archives", "newspapers_periodicals", "web_resources",
        "datasets", "audio", "video", "maps", "relevant_media"
    }
    assert required.issubset({r["source_class"] for r in records})
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["mmsc"]["audited_source_identities"] == 42
    assert status["mmsc"]["raw_web_discovery_records"] == 90
    assert status["mmsc"]["unique_web_discovery_leads"] == 87
    assert status["mmsc"]["duplicate_web_records"] == 3
    assert status["mmsc"]["canonicalized_unique_web_leads"] == 14
    assert status["mmsc"]["unresolved_unique_web_leads"] == 73
    assert status["evidence_and_schema"]["source_claims"] == 52
    assert status["evidence_and_schema"]["evidence_records"] == 52
    assert status["evidence_and_schema"]["evidence_links"] == 52
