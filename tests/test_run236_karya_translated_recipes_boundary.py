from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "karya_endangered_recipes_translated500_mundari_scope_run236_2026-09-12.json"
MMSC = ROOT / "data" / "source_census" / "mmsc_index.json"
METRICS = ROOT / "publication" / "generated" / "release_metrics.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run236_identity_relationship_and_mundari_aggregate_locator():
    audit = load(AUDIT)
    assert audit["run"] == 236
    assert audit["branch"] == "mlhkp-v2"
    assert audit["source"]["repository_id"] == "karya/endangered-recipes-translated-500"
    assert audit["source"]["related_source_dataset"] == "karya/ELR-1000"
    assert audit["deterministic_identity_and_dedup"]["decision"] == "distinct_release_related_to_but_not_identical_with_ELR_1000"
    loc = audit["exact_locator_evidence"]["mundari_aggregate_locator"]
    assert loc == {
        "language": "Mundari",
        "recipes": 50,
        "images": 315,
        "average_images_per_recipe": 6.30,
        "sentence_pairs": 783,
        "evidence_level": "dataset-card aggregate metadata only",
    }


def test_run236_gated_files_do_not_become_record_level_evidence():
    audit = load(AUDIT)
    access = audit["access_and_integrity"]
    rights = audit["rights_and_governance"]
    scope = audit["scope_and_uncertainty"]
    assert access["dataset_files_gated"] is True
    assert access["byte_preserving_acquisition_completed"] is False
    assert access["independent_hash_recomputed"] is False
    assert audit["exact_locator_evidence"]["record_level_rows_or_media_inspected"] == 0
    assert audit["exact_locator_evidence"]["record_level_exact_locators_promoted"] == 0
    assert rights["translated_release_declared_license"] == "CC BY 4.0"
    assert rights["original_elr1000_license_is_separate"] is True
    assert rights["translated_release_license_inferred_to_original_elr1000"] is False
    assert rights["participant_level_consent_artifacts_independently_verified"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_permission_inferred"] is False
    assert scope["cultural_claims_promoted"] == 0
    assert scope["lexical_or_translation_rows_promoted"] == 0
    assert scope["participant_records_promoted"] == 0
    assert scope["images_or_audio_promoted"] == 0


def test_run236_keeps_controlled_counts_synchronized_and_count_neutral():
    audit = load(AUDIT)
    mmsc = load(MMSC)["metrics"]
    metrics = load(METRICS)
    sync = audit["synchronization_decision"]
    assert sync["mmsc_audited_source_identity_count_change"] == 0
    assert sync["source_claim_count_change"] == 0
    assert sync["evidence_record_count_change"] == 0
    assert sync["evidence_link_count_change"] == 0
    assert mmsc["sources_discovered"] == metrics["sources_discovered"] == 42
    assert mmsc["additional_federated_discoveries"] == metrics["additional_federated_discoveries"] == 28
    assert mmsc["still_to_acquire_additional_discoveries"] == metrics["still_to_acquire_additional_discoveries"] == 27
    assert metrics["web_discovery_records_observed"] == 90
    assert metrics["web_discovery_unique_leads"] == 87
    assert metrics["web_discovery_duplicate_records"] == 3
    assert metrics["web_discovery_leads_counted_in_audited_identity_total"] == 14
    assert metrics["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 73
    assert metrics["source_claims"] == metrics["evidence_records"] == metrics["evidence_links"] == 52
    assert metrics["registered_streamlit_modules"] == 42
