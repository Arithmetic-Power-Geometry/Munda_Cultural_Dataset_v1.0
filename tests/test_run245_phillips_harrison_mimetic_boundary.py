from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "phillips_harrison_2017_munda_mimetic_reduplication_run245_2026-09-12.json"
MMSC = ROOT / "data" / "source_census" / "mmsc_index.json"
METRICS = ROOT / "publication" / "generated" / "release_metrics.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run245_exact_publisher_locator():
    audit = load(AUDIT)
    assert audit["run"] == 245
    assert audit["branch"] == "mlhkp-v2"
    assert audit["source"]["doi"] == "10.1017/cnj.2017.13"
    assert audit["source"]["pages"] == "221-242"
    assert audit["identity_and_metadata_verification"]["cambridge_publisher_page_verified"] is True
    assert audit["identity_and_metadata_verification"]["swarthmore_institutional_crosscheck_verified"] is True
    assert audit["identity_and_metadata_verification"]["deterministic_canonical_key"] == "doi:10.1017/cnj.2017.13"
    assert audit["exact_locator_evidence"]["bibliographic_locator_promoted"] is True
    assert "3.2 Verbs" in audit["exact_locator_evidence"]["directly_rendered_article_sections_observed"]
    assert "(13)" in audit["exact_locator_evidence"]["mundari_example_locators_observed"]
    assert "(41)" in audit["exact_locator_evidence"]["kera_mundari_example_locators_observed"]


def test_run245_content_and_cultural_boundary():
    audit = load(AUDIT)
    exact = audit["exact_locator_evidence"]
    boundary = audit["cultural_and_participant_boundary"]
    assert exact["lexical_forms_copied_into_mlhkp"] == 0
    assert exact["claim_level_linguistic_rows_promoted"] == 0
    assert exact["cultural_propositions_promoted"] == 0
    assert exact["underlying_field_recordings_ingested"] == 0
    assert boundary["participant_consent_independently_audited"] is False
    assert boundary["community_validation_independently_audited"] is False
    assert boundary["cultural_access_permission_verified"] is False


def test_run245_rights_are_not_inferred_from_rendering():
    rights = load(AUDIT)["rights_and_access"]
    assert rights["shared_read_only_rendering_observed"] is True
    assert rights["public_availability_is_permission"] is False
    assert rights["redistribution_permission_inferred"] is False
    assert rights["model_training_permission_inferred"] is False
    assert rights["participant_consent_inferred"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_permission_inferred"] is False
    assert rights["full_text_byte_preserving_acquisition_verified"] is False
    assert rights["independent_content_hash_verified"] is False


def test_run245_count_neutral_sync_contract():
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
