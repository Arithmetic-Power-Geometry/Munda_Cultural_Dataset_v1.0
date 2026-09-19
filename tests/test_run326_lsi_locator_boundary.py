import json
from pathlib import Path

AUDIT = Path("data/source_census/lsi_west_bengal_mundari_locator_audit_run326_2026-09-14.json")


def test_run326_lsi_exact_locator_without_overpromotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["source_class"] == "government/TRI/Census/LSI"
    assert d["provider"] == "Office of the Registrar General & Census Commissioner, India (ORGI)"
    assert d["catalog_reference_id"] == "LSI_WB_PART_I"
    assert d["declared_download_filename"] == "LSI_WB_PART_I.pdf"
    assert d["exact_locator"]["section_heading"] == "MUNDARI"
    assert d["exact_locator"]["printed_page"] == 391
    assert d["identity_metadata_verification"]["first_party_catalog_verified"] is True
    assert d["identity_metadata_verification"]["mundari_section_indexed_at_printed_page_391"] is True
    assert d["identity_metadata_verification"]["binary_bytes_acquired_this_run"] is False
    assert d["identity_metadata_verification"]["independent_sha256_verified"] is False
    assert d["identity_metadata_verification"]["printed_page_to_pdf_image_concordance_verified"] is False
    assert d["governance"]["participant_consent_inferred"] is False
    assert d["governance"]["community_validation_inferred"] is False
    assert d["governance"]["cultural_access_authorization_inferred"] is False
    assert d["governance"]["fieldwork_content_promoted"] is False
    assert d["governance"]["cultural_claims_promoted"] is False
    assert d["promotion"]["new_controlled_source_identity"] is False
    assert d["promotion"]["new_controlled_claim"] is False
    assert d["promotion"]["new_evidence_record"] is False
    assert d["promotion"]["new_evidence_link"] is False


def test_run326_search_log_covers_all_controlled_non_mundarica_classes():
    rows = [json.loads(line) for line in Path("data/source_census/search_log_run326.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles", "theses/dissertations",
        "government/TRI/Census/LSI", "archives", "newspapers", "web resources", "datasets",
        "audio", "video", "maps", "relevant media"
    }
    assert len(rows) == 14
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000326" for r in rows)
