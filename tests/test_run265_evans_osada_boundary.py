import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/evans_osada_2005_word_classes_exact_locator_run265_2026-09-12.json"
LOG = ROOT / "data/source_census/search_log_run265.jsonl"


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run265_identity_and_exact_locators():
    d = load_audit()
    assert d["run_id"] == 265
    assert d["source"]["doi"] == "10.1515/lity.2005.9.3.351"
    assert d["source"]["page_range"] == "351-390"
    assert d["source"]["anu_item_uri"] == "http://hdl.handle.net/1885/54663"
    assert d["verified_identity_and_locators"]["article_start_page_locator"] == 351
    assert d["verified_identity_and_locators"]["article_end_page_locator"] == 390
    assert d["verified_identity_and_locators"]["internal_section_locator_from_indexed_published_version"]["page"] == 366
    assert d["verified_identity_and_locators"]["internal_section_locator_from_indexed_published_version"]["section"] == "3.1 Equivalent combinatorics"


def test_run265_rights_integrity_and_cultural_boundaries():
    d = load_audit()
    b = d["rights_access_integrity_boundary"]
    assert b["anu_access_statement_open_access"] is True
    assert b["public_repository_copy_treated_as_blanket_redistribution_license"] is False
    assert b["public_repository_copy_treated_as_model_training_permission"] is False
    assert b["bitstream_bytes_acquired_and_independently_hashed_in_repo"] is False
    assert b["page_image_verification_complete"] is False
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False


def test_run265_zero_unsupported_content_promotion_and_count_neutrality():
    d = load_audit()
    p = d["promotion"]
    assert p["exact_locator_records_promoted"] >= 1
    assert p["controlled_claim_rows_added"] == 0
    assert p["controlled_evidence_rows_added"] == 0
    assert p["controlled_evidence_links_added"] == 0
    assert p["lexical_rows_added"] == 0
    assert p["grammatical_propositions_added"] == 0
    assert p["participant_derived_records_added"] == 0
    assert p["cultural_claims_added"] == 0
    assert d["deduplication"]["canonical_key"] == "doi:10.1515/lity.2005.9.3.351"
    assert d["deduplication"]["identity_count_change"] is False


def test_run265_all_controlled_discovery_classes_logged():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {row["class"] for row in rows}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert classes == expected
    assert all(row["search_id"] == "MMSC-SEARCH-000265" for row in rows)
