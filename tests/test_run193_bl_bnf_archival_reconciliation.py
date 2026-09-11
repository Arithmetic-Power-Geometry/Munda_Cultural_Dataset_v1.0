import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/bl_bnf_durang_kahani_alope_joma_cross_catalogue_run193_2026-09-11.json"
SEARCH = ROOT / "data/source_census/search_log_run193.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run193_exact_archival_locators_and_conservative_reconciliation():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    bl = a["identity_evidence"]["british_library"]
    bnf = a["identity_evidence"]["bnf"]
    assert bl["shelfmark"] == "IOR/S/2/1/17"
    assert bl["record_id"] == "040-000091091"
    assert bl["language_catalogued"] == "Kherwari (Mundari dialect)"
    assert bl["date"] == "1914"
    assert bnf["ark"] == "ark:/12148/cb42562690s"
    assert bnf["notice_number"] == "FRBNF42562690"
    assert bnf["matrix_number"] == "3306Y"
    assert bnf["digital_copy_identifier"] == "NUMAUD-130038"
    assert a["reconciliation"]["decision"].startswith("cross-catalogue historical recording cluster")
    assert a["evidence_promotion"]["count_bearing"] is False


def test_run193_governance_prevents_audio_or_cultural_claim_ingestion():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    g = a["rights_governance"]
    assert g["public_availability_is_permission"] is False
    assert g["copyright_reuse_terms_independently_verified"] is False
    assert g["participant_consent_verified"] is False
    assert g["community_validation_verified"] is False
    assert g["cultural_access_permission_verified"] is False
    assert g["audio_ingested"] is False
    assert g["transcript_ingested"] is False
    assert "cultural meaning/interpretation" in a["evidence_promotion"]["not_promoted"]


def test_run193_all_requested_source_classes_logged_without_count_inflation():
    row = json.loads(SEARCH.read_text(encoding="utf-8").strip())
    required = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI materials",
        "archives", "newspapers/periodicals", "web resources", "datasets",
        "audio", "video", "maps", "relevant media",
    }
    assert required.issubset(set(row["source_classes"]))
    assert row["mmsc_count_change"] == 0
    assert row["source_identity_count_change"] == 0
    assert row["claim_count_change"] == 0
    assert row["evidence_count_change"] == 0
    assert row["publication_numeric_metric_change"] == 0
    assert row["absolute_or_future_proof_completeness_claimed"] is False
    assert row["release_gate"] == "NOT_PASS"


def test_run193_existing_release_counts_remain_locked_until_synchronized_transaction():
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    assert s["mmsc"]["audited_source_identities"] == 42
    assert s["mmsc"]["unresolved_unique_web_leads"] == 73
    assert s["evidence_and_schema"]["source_claims"] == 52
    assert s["evidence_and_schema"]["evidence_records"] == 52
    assert s["streamlit"]["registered_modules"] == 42
    assert s["release_gate"]["status"] == "NOT_PASS"
