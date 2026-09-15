import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run197_volume_xiii_is_secondary_manifestation_only():
    audit = load_json("data/source_census/mundarica_volume_xiii_secondary_manifestation_run197_2026-09-11.json")
    assert audit["result"] == "SECONDARY_DIGITIZED_MANIFESTATION_VERIFIED_NOT_AUTHORITATIVE"

    manifestation = audit["manifestation"]
    assert manifestation["internet_archive_identifier"] == "dli.ernet.14932"
    assert manifestation["identifier_ark"] == "ark:/13960/t6r01q423"
    assert manifestation["source"] == "Digital Library of India"
    assert manifestation["scanning_centre"] == "C-DAC, Noida"
    assert manifestation["source_library"] == "Lbs National Academy Of Administration"
    assert manifestation["ppi_as_catalogued"] == 600
    assert manifestation["ocr_converted_as_catalogued"] == "abbyy-to-hocr 1.1.37"
    assert manifestation["pdf_degraded_as_catalogued"] == "invalid-jp2-headers"

    boundary = audit["verification_boundary"]
    assert boundary["secondary_item_identity_verified"] is True
    assert boundary["repository_catalogue_metadata_verified"] is True
    assert boundary["catalogued_pdf_degradation_warning_preserved"] is True
    assert boundary["authoritative_physical_copy_comparison"] is False
    assert boundary["authoritative_scan_registered"] is False
    assert boundary["independent_byte_hash_verified"] is False
    assert boundary["catalogued_scan_page_count_verified"] is False
    assert boundary["ocr_treated_as_verified_transcription"] is False
    assert boundary["verified_complete_volume"] is False
    assert boundary["cultural_passages_ingested"] is False
    assert boundary["claims_added"] == 0
    assert boundary["evidence_records_added"] == 0
    assert boundary["evidence_links_added"] == 0
    assert boundary["source_identity_added"] is False

    rights = audit["rights_and_governance"]
    assert rights["repository_visibility_treated_as_reuse_permission"] is False
    assert rights["download_option_visibility_treated_as_reuse_permission"] is False
    assert rights["derivative_availability_treated_as_cultural_access_permission"] is False
    assert rights["participant_consent_inferred"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_inferred"] is False
    assert rights["cultural_access_overrides_entitlement"] is True


def test_run197_search_log_covers_all_requested_classes_and_preserves_counts():
    log_path = ROOT / "data/source_census/search_log_run197.jsonl"
    record = json.loads(log_path.read_text(encoding="utf-8").strip())
    assert record["search_id"] == "MMSC-SEARCH-000197"
    requested = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI materials",
        "archives", "newspapers/periodicals", "web resources", "datasets",
        "audio", "video", "maps", "relevant media"
    }
    assert requested.issubset(set(record["source_classes"]))
    metrics = record["controlled_metrics"]
    assert metrics["audited_source_identities"] == 42
    assert metrics["raw_web_discovery_records"] == 90
    assert metrics["unique_web_discovery_leads"] == 87
    assert metrics["duplicate_web_records"] == 3
    assert metrics["canonicalized_unique_web_leads"] == 14
    assert metrics["unresolved_unique_web_leads"] == 73
    assert metrics["source_claims"] == 52
    assert metrics["evidence_records"] == 52
    assert metrics["evidence_links"] == 52
    assert metrics["streamlit_modules"] == 42
    assert record["release_gate"] == "NOT_PASS"


def test_run197_status_never_promotes_mundarica_completeness():
    status = load_json("status/mlhkp_progress.json")
    assert status["mundarica"]["authoritative_scans_registered"] == 0
    assert status["mundarica"]["verified_complete_volumes"] == 0
    assert status["mundarica"]["ocr_is_not_verified_transcription"] is True
    assert status["release_gate"]["status"] == "NOT_PASS"
