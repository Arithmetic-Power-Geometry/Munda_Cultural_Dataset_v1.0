import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run199_ciil_exact_manifestations_are_cover_only_and_non_count_bearing():
    audit = load_json("data/source_census/ciil_sanchika_mundari_language_books_manifestation_run199_2026-09-11.json")
    assert audit["result"] == "TWO_EXACT_CIIL_SANCHIKA_MANIFESTATIONS_VERIFIED_METADATA_AND_COVER_ONLY"
    assert len(audit["items"]) == 2

    by_id = {item["repository_identifier"]: item for item in audit["items"]}
    soy = by_id["BVP04859"]
    assert soy["handle"] == "20.500.14705/11519"
    assert soy["repository_file"] == "BVP04859.pdf"
    assert soy["retrieved_pdf_pages_observed"] == 1
    assert soy["rights_holder_as_catalogued"] == "Birendra Kumar Soy 'Munda'"

    word_book = by_id["BVP00242"]
    assert word_book["handle"] == "20.500.14705/8437"
    assert word_book["repository_file"] == "BVP00242.pdf"
    assert word_book["retrieved_pdf_pages_observed"] == 1
    assert word_book["rights_holder_as_catalogued"] == "Bharat Munda Samaj"

    boundary = audit["verification_boundary"]
    assert boundary["institutional_repository_identity_verified"] is True
    assert boundary["direct_bitstream_resolved"] is True
    assert boundary["cover_page_visually_verified"] is True
    assert boundary["full_book_text_verified"] is False
    assert boundary["retrieved_one_page_pdf_treated_as_complete_book"] is False
    assert boundary["independent_byte_hash_verified"] is False
    assert boundary["grammar_rules_ingested"] is False
    assert boundary["lexical_entries_ingested"] is False
    assert boundary["cultural_claims_ingested"] is False
    assert boundary["claims_added"] == 0
    assert boundary["evidence_records_added"] == 0
    assert boundary["evidence_links_added"] == 0
    assert boundary["source_identities_added"] == 0

    rights = audit["rights_and_governance"]
    assert rights["public_file_visibility_treated_as_reuse_permission"] is False
    assert rights["open_license_verified"] is False
    assert rights["model_training_permission_inferred"] is False
    assert rights["participant_consent_inferred"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_permission_inferred"] is False
    assert rights["cultural_access_overrides_technical_availability"] is True


def test_run199_all_requested_classes_and_count_contract_are_logged():
    raw = (ROOT / "data/source_census/search_log_run199.jsonl").read_text(encoding="utf-8").strip()
    log = json.loads(raw)
    requested = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI materials",
        "archives", "newspapers/periodicals", "web resources", "datasets",
        "audio", "video", "maps", "relevant media"
    }
    assert requested.issubset(set(log["source_classes"]))
    assert log["mmsc_count_change"] == 0
    assert log["source_identity_count_change"] == 0
    assert log["claim_count_change"] == 0
    assert log["evidence_count_change"] == 0
    assert log["evidence_link_count_change"] == 0
    metrics = log["controlled_metrics"]
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
    assert log["release_gate"] == "NOT_PASS"
