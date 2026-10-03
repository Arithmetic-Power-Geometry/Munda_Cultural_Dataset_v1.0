import json
from pathlib import Path


def test_run290_bhaduri_dictionary_boundary():
    p = Path("data/source_census/bhaduri_mundari_english_dictionary_edition_lineage_run290_2026-09-13.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["run_id"] == 290
    assert data["identity_reconciliation"]["same_work_supported"] is True
    assert data["identity_reconciliation"]["manifestations_must_not_be_counted_as_distinct_works"] is True
    assert data["promotion"]["lexical_entries_promoted"] == 0
    assert data["access_and_rights"]["primary_1931_bytes_acquired"] is False
    assert data["access_and_rights"]["independent_file_hash_verified"] is False
    assert data["access_and_rights"]["cultural_access_permission_inferred"] is False
