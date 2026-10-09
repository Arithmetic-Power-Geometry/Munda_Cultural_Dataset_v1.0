from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "choksi_2020_mundari_expressives_exact_locator_run241_2026-09-12.json"
MMSC = ROOT / "data" / "source_census" / "mmsc_index.json"
METRICS = ROOT / "publication" / "generated" / "release_metrics.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run241_exact_bibliographic_locator():
    audit = load(AUDIT)
    assert audit["run"] == 241
    assert audit["branch"] == "mlhkp-v2"
    assert audit["source"]["doi"] == "10.1017/S0047404519000824"
    assert audit["source"]["pages"] == "379-398"
    assert audit["identity_and_metadata_verification"]["publisher_page_verified"] is True
    assert audit["identity_and_metadata_verification"]["doi_verified"] is True
    assert audit["exact_locator_evidence"]["bibliographic_locator_promoted"] is True
    assert audit["exact_locator_evidence"]["abstract_level_scope_verified"] is True


def test_run241_participant_media_boundary():
    audit = load(AUDIT)
    exact = audit["exact_locator_evidence"]
    gate = audit["participant_and_cultural_boundary"]
    assert exact["raw_video_or_interview_content_ingested"] is False
    assert exact["linguistic_or_cultural_propositions_promoted"] == 0
    assert gate["participant_consent_independently_audited"] is False
    assert gate["raw_recording_rights_verified"] is False
    assert gate["community_validation_independently_audited"] is False
    assert gate["cultural_access_permission_verified"] is False


def test_run241_rights_are_not_inferred_from_visibility():
    rights = load(AUDIT)["rights_and_access"]
    assert rights["public_availability_is_permission"] is False
    assert rights["redistribution_permission_inferred"] is False
    assert rights["model_training_permission_inferred"] is False
    assert rights["participant_consent_inferred"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_permission_inferred"] is False


def test_run241_count_neutral_sync_contract():
    audit = load(AUDIT)
    sync = audit["synchronization_decision"]
    mmsc = load(MMSC)["metrics"]
    metrics = load(METRICS)
    assert sync["mmsc_audited_source_identity_count_change"] == 0
    assert sync["source_claim_count_change"] == 0
    assert sync["evidence_record_count_change"] == 0
    assert sync["evidence_link_count_change"] == 0
    assert mmsc["sources_discovered"] == metrics["sources_discovered"] == 42
    assert metrics["web_discovery_records_observed"] == 90
    assert metrics["web_discovery_unique_leads"] == 87
    assert metrics["web_discovery_duplicate_records"] == 3
    assert metrics["web_discovery_leads_counted_in_audited_identity_total"] == 14
    assert metrics["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 73
    assert metrics["source_claims"] == metrics["evidence_records"] == metrics["evidence_links"] == 52
    assert metrics["registered_streamlit_modules"] == 42
