import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/nirang_pajhra_authoritative_registration_retry_run162_2026-09-10.json"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run162_nirang_remains_blocked_without_authoritative_record():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["candidate"] == "Nirang Pajhra"
    assert data["reported_registration_identifier_from_secondary_source"] == "WBMUL00610"
    assert data["authoritative_registration_search"]["authoritative_prgi_or_rni_record_resolved"] is False
    assert data["deterministic_disposition"] == "candidate_blocked_pending_authoritative_registration_or_issue_manifestation"
    assert data["content_ingested"] is False
    assert data["claims_promoted"] == 0
    assert data["source_identity_count_change"] == 0
    assert data["evidence_count_change"] == 0


def test_run162_nirang_does_not_overclaim_rights_language_or_validation():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["rights_verified"] is False
    assert data["community_validation_verified"] is False
    assert data["cultural_access_verified"] is False
    boundary = data["verification_boundary"].lower()
    assert "registration" in boundary
    assert "mundari" in boundary
    assert "permission" in boundary
    assert "community validation" in boundary


def test_run162_status_counts_remain_defensible():
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["latest_run"] >= 161
    assert status["mmsc"]["audited_source_identities"] == 41
    assert status["mmsc"]["raw_web_discovery_records"] == 90
    assert status["mmsc"]["unique_web_discovery_leads"] == 87
    assert status["mmsc"]["duplicate_web_records"] == 3
    assert status["mmsc"]["canonicalized_unique_web_leads"] == 13
    assert status["mmsc"]["unresolved_unique_web_leads"] == 74
    assert status["evidence_and_schema"]["source_claims"] == 52
    assert status["streamlit"]["registered_modules"] == 42
