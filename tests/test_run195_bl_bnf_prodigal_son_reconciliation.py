import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/bl_bnf_prodigal_son_mundari_cross_catalogue_run195_2026-09-11.json"
SEARCH = ROOT / "data/source_census/search_log_run195.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run195_matrix_level_cross_catalogue_reconciliation_is_deterministic():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    bl = a["identity_evidence"]["british_library"]
    bnf = a["identity_evidence"]["bnf"]
    assert bl["shelfmark"] == "IOR/S/2/1/2"
    assert bl["record_id"] == "040-000091076"
    assert bl["mdark"] == "ark:/81055/vdc_100000000502.0x0002fd"
    assert bl["former_external_reference"].replace("-", "") == "3290Y"
    assert bnf["ark"] == "ark:/12148/cb414605823"
    assert bnf["notice_number"] == "FRBNF41460582"
    assert bnf["matrix_number"] == "3290Y"
    assert bnf["digital_copy_identifier"] == "NUMAUD-129811"
    assert bnf["physical_copy_identifier"] == "AP-2102"
    assert bl["former_external_reference"].replace("-", "") == bnf["matrix_number"]
    assert a["reconciliation"]["byte_or_physical_identity_verified"] is False
    assert a["evidence_promotion"]["count_bearing"] is False


def test_run195_governance_blocks_audio_transcript_and_cultural_promotion():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    g = a["rights_governance"]
    assert g["public_availability_is_permission"] is False
    assert g["bl_catalogue_text_cc_by_treated_as_audio_license"] is False
    assert g["bl_public_record_status_treated_as_reuse_license"] is False
    assert g["bnf_online_access_treated_as_reuse_license"] is False
    assert g["sound_recording_reuse_terms_independently_verified"] is False
    assert g["participant_consent_verified"] is False
    assert g["community_validation_verified"] is False
    assert g["cultural_access_permission_verified"] is False
    assert g["audio_ingested"] is False
    assert g["transcript_ingested"] is False
    assert g["translation_ingested"] is False
    assert "cultural interpretation" in a["evidence_promotion"]["not_promoted"]


def test_run195_systematic_census_preserves_counts_and_release_gate():
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
    assert row["evidence_link_count_change"] == 0
    assert row["publication_numeric_metric_change"] == 0
    assert row["absolute_or_future_proof_completeness_claimed"] is False
    assert row["release_gate"] == "NOT_PASS"
    m = row["controlled_metrics"]
    assert m["audited_source_identities"] == 42
    assert m["raw_web_discovery_records"] == 90
    assert m["unique_web_discovery_leads"] == 87
    assert m["duplicate_web_records"] == 3
    assert m["canonicalized_unique_web_leads"] == 14
    assert m["unresolved_unique_web_leads"] == 73
    assert m["source_claims"] == 52
    assert m["evidence_records"] == 52
    assert m["evidence_links"] == 52
    assert m["streamlit_modules"] == 42


def test_run195_primary_status_has_not_drifted_before_status_sync():
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    assert s["branch"] == "mlhkp-v2"
    assert s["mmsc"]["audited_source_identities"] == 42
    assert s["mmsc"]["unresolved_unique_web_leads"] == 73
    assert s["evidence_and_schema"]["source_claims"] == 52
    assert s["evidence_and_schema"]["evidence_records"] == 52
    assert s["streamlit"]["registered_modules"] == 42
    assert s["release_gate"]["status"] == "NOT_PASS"
