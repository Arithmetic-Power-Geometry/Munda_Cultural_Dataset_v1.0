import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/ezcc_folk_dances_manifestation_rights_exact_locator_run161_2026-09-10.json"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run161_audit_identity_and_locators():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["canonical_source_id"] == "SRC-MMSC-000015"
    assert data["reconciled_web_source_id"] == "WEB-MUN-0047"
    assert data["origin_video_id"] == "jcaVTX0BCtQ"
    assert data["license_verification"]["file_level_license"] == "CC BY 3.0 Unported"
    labels = {(x["timestamp"], x["repository_label"]) for x in data["exact_repository_locators"]}
    assert ("00:04:28", "Paika (Munda community)") in labels
    assert ("00:06:00", "Mundari") in labels
    assert ("00:11:12", "Mundari (Marriage)") in labels


def test_run161_does_not_overclaim_rights_or_culture():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["manifestation"]["locally_downloaded"] is False
    assert data["manifestation"]["independent_file_hash_computed"] is False
    assert data["promotion_decision"]["evidence_count_change"] == 0
    assert data["promotion_decision"]["source_identity_count_change"] == 0
    excluded = " ".join(data["license_verification"]["does_not_establish"]).lower()
    assert "consent" in excluded
    assert "community" in excluded
    assert "cultur" in excluded


def test_run161_status_contract():
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["latest_run"] >= 161
    assert status["mmsc"]["audited_source_identities"] == 41
    assert status["mmsc"]["raw_web_discovery_records"] == 90
    assert status["mmsc"]["unique_web_discovery_leads"] == 87
    assert status["mmsc"]["duplicate_web_records"] == 3
    assert status["mmsc"]["canonicalized_unique_web_leads"] == 13
    assert status["mmsc"]["unresolved_unique_web_leads"] == 74
    assert status["evidence_and_schema"]["source_claims"] == 52
    assert status["evidence_and_schema"]["evidence_records"] == 52
    assert status["streamlit"]["registered_modules"] == 42
    assert status["streamlit"]["mapped_modules"] == 42
