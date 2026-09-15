import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/bl_bnf_a_kahani_cross_catalogue_run194_2026-09-11.json"
SEARCH = ROOT / "data/source_census/search_log_run194.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run194_matrix_level_cross_catalogue_reconciliation_is_deterministic():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    bl = a["identity_evidence"]["british_library"]
    bnf = a["identity_evidence"]["bnf"]
    assert bl["shelfmark"] == "IOR/S/2/1/4"
    assert bl["record_id"] == "040-000091078"
    assert bl["former_external_reference"].replace("-", "") == "3292Y"
    assert bnf["ark"] == "ark:/12148/cb41463717x"
    assert bnf["notice_number"] == "FRBNF41463717"
    assert bnf["matrix_number"] == "3292Y"
    assert bl["former_external_reference"].replace("-", "") == bnf["matrix_number"]
    assert a["reconciliation"]["byte_or_physical_identity_verified"] is False
    assert a["evidence_promotion"]["count_bearing"] is False


def test_run194_governance_blocks_audio_transcript_and_cultural_promotion():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    g = a["rights_governance"]
    assert g["public_availability_is_permission"] is False
    assert g["bl_public_record_status_treated_as_reuse_license"] is False
    assert g["copyright_reuse_terms_independently_verified"] is False
    assert g["participant_consent_verified"] is False
    assert g["community_validation_verified"] is False
    assert g["cultural_access_permission_verified"] is False
    assert g["audio_ingested"] is False
    assert g["transcript_ingested"] is False
    assert "cultural interpretation" in a["evidence_promotion"]["not_promoted"]


def test_run194_mundarica_vii_candidate_does_not_fake_verification():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    m = a["mundarica_parallel_stream"]
    assert m["volume_vii_candidate_secondary_identifier"] == "dli.bengal.10689.20088"
    assert m["direct_archive_metadata_verified_this_run"] is False
    assert m["page_count_promoted"] is False
    assert m["ocr_state_promoted"] is False
    assert m["rights_state_promoted"] is False
    assert m["completeness_promoted"] is False


def test_run194_systematic_census_preserves_release_counts_and_gate():
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

    s = json.loads(STATUS.read_text(encoding="utf-8"))
    assert s["mmsc"]["audited_source_identities"] == 42
    assert s["mmsc"]["unresolved_unique_web_leads"] == 73
    assert s["evidence_and_schema"]["source_claims"] == 52
    assert s["evidence_and_schema"]["evidence_records"] == 52
    assert s["streamlit"]["registered_modules"] == 42
    assert s["release_gate"]["status"] == "NOT_PASS"
