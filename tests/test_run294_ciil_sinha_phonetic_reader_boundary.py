import json
from pathlib import Path


def test_run294_sinha_phonetic_reader_metadata_boundary():
    data = json.loads(Path("data/source_census/ciil_sinha_mundari_phonetic_reader_metadata_audit_run294_2026-09-13.json").read_text(encoding="utf-8"))
    assert data["run_id"] == 294
    assert data["canonical_work"]["title"] == "Mundari Phonetic Reader"
    assert data["canonical_work"]["author"] == "N. K. Sinha"
    assert data["canonical_work"]["year"] == 1974
    assert data["canonical_work"]["series_number"] == 13
    assert data["deterministic_identity_decision"]["same_work"] is True
    assert data["deterministic_identity_decision"]["separate_source_identity_created"] is False
    assert data["pagination_uncertainty"]["first_party_catalogue"] == "102 pages"
    assert data["pagination_uncertainty"]["cinii"] == "viii, 102 p."
    assert data["pagination_uncertainty"]["cambridge_review"] == "xi, 103 pp."
    assert data["promotion"]["controlled_lexical_rows_added"] == 0
    assert data["promotion"]["controlled_cultural_claims_added"] == 0
    assert data["promotion"]["primary_text_promoted"] is False
    assert data["rights_access_governance"]["primary_book_bytes_acquired"] is False
    assert data["rights_access_governance"]["primary_book_hash_verified"] is False
    assert data["rights_access_governance"]["participant_consent_inferred"] is False
    assert data["rights_access_governance"]["community_validation_inferred"] is False
    assert data["rights_access_governance"]["cultural_access_permission_inferred"] is False


def test_run294_has_fourteen_search_classes():
    rows = [json.loads(line) for line in Path("data/source_census/search_log_run294.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert len({row["class"] for row in rows}) == 14
    assert {row["run_id"] for row in rows} == {294}
