import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run200_ciil_sinha_tirki_exact_locator_boundary():
    audit = load_json("data/source_census/ciil_sinha_tirki_mundari_grammar_manifestation_run200_2026-09-11.json")
    assert audit["result"] == "TWO_CIIL_GRAMMAR_MANIFESTATIONS_EXACT_LOCATED_WITH_COVER_ONLY_BOUNDARY"
    by_id = {item["repository_identifier"]: item for item in audit["items"]}

    sinha = by_id["CIILP0091"]
    assert sinha["handle"] == "20.500.14705/8179"
    assert sinha["catalogued_extent"] == 176
    assert sinha["retrieved_pdf_pages_observed"] == 1
    assert sinha["repository_file"] == "CIILP0091.pdf"

    tirki = by_id["BVP03961"]
    assert tirki["handle"] == "20.500.14705/8450"
    assert tirki["rights_holder_as_catalogued"] == "Sikradas Tirki"
    assert tirki["retrieved_pdf_pages_observed"] == 1
    assert tirki["repository_file"] == "BVP03961.pdf"

    boundary = audit["verification_boundary"]
    assert boundary["institutional_repository_identity_verified"] is True
    assert boundary["direct_bitstreams_resolved"] is True
    assert boundary["cover_pages_visually_verified"] is True
    assert boundary["catalogued_extent_treated_as_retrieved_page_count"] is False
    assert boundary["retrieved_one_page_pdfs_treated_as_complete_books"] is False
    assert boundary["independent_byte_hash_verified"] is False
    assert boundary["full_book_page_sequence_verified"] is False
    assert boundary["grammar_passages_page_verified"] is False
    assert boundary["grammar_rules_ingested"] is False
    assert boundary["lexical_entries_ingested"] is False
    assert boundary["cultural_claims_ingested"] is False
    assert boundary["source_identities_added"] == 0
    assert boundary["claims_added"] == 0
    assert boundary["evidence_records_added"] == 0
    assert boundary["evidence_links_added"] == 0

    rights = audit["rights_and_governance"]
    assert rights["public_file_visibility_treated_as_reuse_permission"] is False
    assert rights["exact_license_text_verified"] is False
    assert rights["model_training_permission_inferred"] is False
    assert rights["participant_consent_inferred"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_permission_inferred"] is False


def test_run200_all_requested_classes_and_zero_count_inflation_are_logged():
    log = json.loads((ROOT / "data/source_census/search_log_run200.jsonl").read_text(encoding="utf-8").strip())
    requested = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI materials",
        "archives", "newspapers/periodicals", "web resources", "datasets",
        "audio", "video", "maps", "relevant media"
    }
    assert requested.issubset(set(log["classes"]))
    assert log["search_id"] == "MMSC-SEARCH-000200"
    for value in log["count_change"].values():
        assert value == 0
    assert log["principles"]["no_fabricated_counts"] is True
    assert log["principles"]["no_fabricated_cultural_claims"] is True
    assert log["principles"]["blocked_sources_logged_and_bypassed"] is True
    assert log["principles"]["public_availability_is_not_permission"] is True
