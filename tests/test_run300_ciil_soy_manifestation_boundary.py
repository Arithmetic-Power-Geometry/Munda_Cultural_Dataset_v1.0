import json
from pathlib import Path


def test_run300_ciil_soy_manifestation_boundary():
    data = json.loads(Path("data/source_census/ciil_soy_mundari_linguistic_structure_manifestation_run300_2026-09-13.json").read_text(encoding="utf-8"))
    assert data["run_id"] == 300
    assert data["source"]["repository_identifier"] == "BVP04859"
    assert data["source"]["repository_file_name"] == "BVP04859.pdf"
    assert data["identity_and_metadata_verification"]["first_party_repository_metadata_verified"] is True
    assert data["direct_manifestation_check"]["viewer_reported_page_count"] == 1
    assert data["direct_manifestation_check"]["page_1_is_cover_image"] is True
    assert data["direct_manifestation_check"]["full_book_bytes_verified"] is False
    assert data["access_and_rights"]["bulk_text_reuse_permission_verified"] is False
    assert data["promotion"]["primary_book_text_promoted"] == 0
    assert data["promotion"]["controlled_claims_added"] == 0
    assert data["scope_and_cultural_boundary"]["participant_consent_inferred"] is False
    assert data["scope_and_cultural_boundary"]["community_validation_inferred"] is False
    assert data["scope_and_cultural_boundary"]["cultural_access_permission_inferred"] is False


def test_run300_has_fourteen_search_classes():
    rows = [json.loads(line) for line in Path("data/source_census/search_log_run300.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert len({row["class"] for row in rows}) == 14
    assert {row["search_id"] for row in rows} == {"MMSC-SEARCH-000300"}
