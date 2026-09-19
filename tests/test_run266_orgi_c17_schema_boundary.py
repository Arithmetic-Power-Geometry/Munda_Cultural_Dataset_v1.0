import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/orgi_c17_jharkhand_full_schema_locator_run266_2026-09-12.json"
LOG = ROOT / "data/source_census/search_log_run266.jsonl"


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run266_official_identity_and_schema_locators():
    d = load_audit()
    assert d["run_id"] == 266
    assert d["source"]["reference_id"] == "PC11_C17-20"
    assert d["source"]["declared_download_filename"] == "DDW-C17-2000.XLSX"
    s = d["verified_schema"]
    assert "MUNDA" in s["target_categories"]["total_speakers"]
    assert "MUNDARI" in s["target_categories"]["total_speakers"]
    assert "MUNDA" in s["target_categories"]["first_subsidiary_language"]
    assert "MUNDARI" in s["target_categories"]["second_subsidiary_language"]
    assert s["munda_and_mundari_are_distinct_catalogue_labels"] is True
    assert s["person_male_female_breakout_declared"] is True


def test_run266_no_unverified_numeric_or_integrity_promotion():
    d = load_audit()
    s = d["verified_schema"]
    b = d["integrity_and_rights_boundary"]
    p = d["promotion"]
    assert s["numeric_values_verified"] is False
    assert s["worksheet_names_verified"] is False
    assert s["exact_cell_coordinates_verified"] is False
    assert b["workbook_bytes_acquired"] is False
    assert b["independent_cryptographic_hash_verified"] is False
    assert b["numeric_cell_values_promoted"] is False
    assert p["numeric_values_added"] == 0
    assert p["controlled_claim_rows_added"] == 0
    assert p["controlled_evidence_rows_added"] == 0
    assert p["cultural_claims_added"] == 0


def test_run266_rights_and_cultural_access_boundaries():
    b = load_audit()["integrity_and_rights_boundary"]
    assert b["catalogue_metadata_treated_as_permission_for_blanket_redistribution"] is False
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False


def test_run266_count_neutral_and_all_controlled_classes_logged():
    d = load_audit()
    assert d["deduplication"]["canonical_key"] == "orgi:PC11_C17-20"
    assert d["deduplication"]["identity_count_change"] is False
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {row["class"] for row in rows}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert classes == expected
    assert all(row["search_id"] == "MMSC-SEARCH-000266" for row in rows)
