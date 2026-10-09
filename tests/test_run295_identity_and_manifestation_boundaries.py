import json
from pathlib import Path


def test_run295_south_sudan_name_collision_is_excluded():
    data = json.loads(Path("data/source_census/mundari_name_collision_south_sudan_exclusion_run295_2026-09-13.json").read_text(encoding="utf-8"))
    assert data["run_id"] == 295
    assert data["deterministic_disposition"]["same_identity_as_munda_mundari"] is False
    assert data["deterministic_disposition"]["canonicalize_into_mlhkp_mundari"] is False
    assert data["deterministic_disposition"]["eligible_for_mlhkp_cultural_evidence"] is False
    assert data["promotion"]["new_controlled_source_identity"] is False
    assert data["promotion"]["new_cultural_claim"] is False
    assert data["governance"]["prevents_cross_community_contamination"] is True


def test_run295_retailer_metadata_does_not_promote_primary_content():
    data = json.loads(Path("data/source_census/ciil_sinha_phonetic_reader_retail_manifestation_audit_run295_2026-09-13.json").read_text(encoding="utf-8"))
    assert data["run_id"] == 295
    assert data["deterministic_identity_decision"]["new_audited_source_identity_added"] is False
    assert data["promotion"]["bibliographic_manifestation_metadata_only"] is True
    assert data["promotion"]["primary_bytes_acquired"] is False
    assert data["promotion"]["independent_hash_verified"] is False
    assert data["promotion"]["ocr_verified"] is False
    assert data["promotion"]["lexical_or_phonetic_content_promoted"] is False
    assert data["promotion"]["cultural_claim_promoted"] is False
    assert data["rights_governance"]["retail_availability_is_not_reuse_permission"] is True


def test_run295_has_fourteen_search_classes():
    rows = [json.loads(line) for line in Path("data/source_census/search_log_run295.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert len({row["class"] for row in rows}) == 14
    assert {row["run_id"] for row in rows} == {295}
