import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run192_volume_vi_is_secondary_only():
    audit = load_json("data/source_census/mundarica_volume_vi_secondary_manifestation_run192_2026-09-11.json")
    assert audit["volume"] == "VI"
    assert audit["result"] == "SECONDARY_DIGITIZED_MANIFESTATION_VERIFIED_NOT_AUTHORITATIVE"
    m = audit["manifestation"]
    assert m["internet_archive_identifier"] == "dli.bengal.10689.20084"
    assert m["dli_handle"] == "10689/20084"
    assert m["total_scan_pages_as_catalogued"] == 344
    assert m["ppi_as_catalogued"] == 600
    assert "ABBYY FineReader 11.0" in m["ocr_as_catalogued"]

    boundary = audit["verification_boundary"]
    assert boundary["secondary_item_identity_verified"] is True
    assert boundary["catalogued_page_accounting_verified"] is True
    assert boundary["authoritative_physical_copy_comparison"] is False
    assert boundary["authoritative_scan_registered"] is False
    assert boundary["independent_byte_hash_verified"] is False
    assert boundary["ocr_treated_as_verified_transcription"] is False
    assert boundary["verified_complete_volume"] is False
    assert boundary["cultural_passages_ingested"] is False
    assert boundary["claims_added"] == 0
    assert boundary["evidence_records_added"] == 0
    assert boundary["source_identity_added"] is False

    rights = audit["rights_and_governance"]
    assert rights["repository_visibility_treated_as_reuse_permission"] is False
    assert rights["derivative_availability_treated_as_cultural_access_permission"] is False
    assert rights["participant_consent_inferred"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_inferred"] is False
    assert rights["cultural_access_overrides_entitlement"] is True


def test_run192_status_never_promotes_mundarica_completeness():
    status = load_json("status/mlhkp_progress.json")
    assert status["mundarica"]["authoritative_scans_registered"] == 0
    assert status["mundarica"]["verified_complete_volumes"] == 0
    assert status["mundarica"]["ocr_is_not_verified_transcription"] is True
    assert status["release_gate"]["status"] == "NOT_PASS"
