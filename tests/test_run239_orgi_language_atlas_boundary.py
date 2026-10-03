from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "orgi_language_atlas_2011_manifestation_run239_2026-09-12.json"
MMSC = ROOT / "data" / "source_census" / "mmsc_index.json"
METRICS = ROOT / "publication" / "generated" / "release_metrics.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run239_official_identity_and_manifest_locator():
    audit = load(AUDIT)
    assert audit["run"] == 239
    assert audit["branch"] == "mlhkp-v2"
    assert audit["source"]["reference_id"] == "Language_Atlas_2011"
    assert audit["source"]["catalog_id"] == 42561
    assert audit["source"]["declared_file"] == "Language_Atlas_2011.pdf"
    assert audit["identity_and_metadata_verification"]["official_catalog_record_verified"] is True
    assert audit["exact_locator_evidence"]["catalog_level_locator_promoted"] is True


def test_run239_gateway_block_prevents_internal_content_promotion():
    audit = load(AUDIT)
    blocked = audit["blocked_acquisition"]
    exact = audit["exact_locator_evidence"]
    assert blocked["byte_preserving_acquisition_completed"] is False
    assert blocked["independent_hash_recomputed"] is False
    assert blocked["page_image_verification_completed"] is False
    assert exact["internal_page_or_map_locators_verified_from_official_pdf"] == []
    assert exact["numeric_values_promoted"] == 0
    assert exact["mundari_or_munda_demographic_claims_promoted"] == 0


def test_run239_rights_and_cultural_gates_remain_independent():
    rights = load(AUDIT)["rights_and_governance"]
    assert rights["public_availability_is_permission"] is False
    assert rights["redistribution_permission_inferred"] is False
    assert rights["model_training_permission_inferred"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["participant_consent_inferred"] is False
    assert rights["cultural_access_permission_inferred"] is False


def test_run239_count_neutral_sync_contract():
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
