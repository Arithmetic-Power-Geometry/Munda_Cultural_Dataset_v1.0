import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "lsi_west_bengal_mundari_exact_locator_run263_2026-09-12.json"
LOG = ROOT / "data" / "source_census" / "search_log_run263.jsonl"


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run263_exact_official_identity_and_mundari_locators():
    d = load_audit()
    assert d["run_id"] == 263
    src = d["source"]
    assert src["catalogue_id"] == "LSI_WB_PART_I"
    assert src["declared_download"] == "LSI_WB_PART_I.pdf"
    assert src["date_published"] == "2016-08-01"
    assert src["mundari_section_author_as_rendered"] == "SIBASIS MUKHERJEE"
    locators = {x["locator"] for x in d["exact_locators"]}
    assert any("p.391" in x and "MUNDARI" in x for x in locators)
    assert any("p.391" in x and "1.1 FAMILY AFFILIATION" in x for x in locators)
    assert any("p.391" in x and "1.2 LOCATION" in x for x in locators)


def test_run263_fieldwork_provenance_is_not_participant_content():
    d = load_audit()
    pctx = d["participant_and_sensitive_context"]
    assert pctx["named_historical_informants_visible_in_public_source"] is True
    assert pctx["names_repeated_into_controlled_dataset"] is False
    assert pctx["participant_consent_independently_verified"] is False
    assert pctx["community_validation_verified"] is False
    assert pctx["cultural_access_permission_verified"] is False
    assert pctx["participant_derived_content_ingested"] is False
    joined = " ".join(x["supported_metadata_or_scope"] for x in d["exact_locators"])
    assert "Jhargram" in joined
    assert "August 1995" in joined


def test_run263_rights_integrity_boundary_and_blocked_pdf_are_explicit():
    d = load_audit()
    b = d["rights_access_integrity_boundary"]
    assert b["first_party_catalogue_verified"] is True
    assert b["first_party_direct_pdf_identity_verified"] is True
    assert b["complete_pdf_bytes_acquired_byte_preservingly"] is False
    assert b["independent_cryptographic_hash_verified"] is False
    assert b["page_image_verified_in_this_run"] is False
    assert b["ocr_against_page_image_verified"] is False
    assert b["explicit_redistribution_license_verified"] is False
    assert b["model_training_permission_verified"] is False
    assert len(d["blocked_attempts"]) == 1
    assert "timed out" in d["blocked_attempts"][0]["observation"].lower()


def test_run263_promotion_is_beyond_discovery_but_zero_content_claims():
    d = load_audit()
    p = d["promotion"]
    assert p["discovery_only"] is False
    assert p["exact_locator_records_promoted"] == 4
    assert p["controlled_claim_rows_added"] == 0
    assert p["controlled_evidence_rows_added"] == 0
    assert p["controlled_evidence_links_added"] == 0
    assert p["lexical_rows_promoted"] == 0
    assert p["grammatical_propositions_promoted"] == 0
    assert p["demographic_values_promoted"] == 0
    assert p["participant_derived_records_promoted"] == 0
    assert p["cultural_claims_promoted"] == 0
    assert d["deduplication"]["identity_count_change"] is False


def test_run263_search_log_covers_all_required_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {row["class"] for row in rows}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert classes == expected
    assert len(rows) == 14
    assert all(row["search_id"] == "MMSC-SEARCH-000263" for row in rows)
