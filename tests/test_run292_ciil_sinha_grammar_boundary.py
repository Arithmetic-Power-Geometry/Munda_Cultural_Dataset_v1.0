import json
from pathlib import Path


def test_run292_ciil_sinha_locator():
    data = json.loads(Path("data/source_census/ciil_sinha_mundari_grammar_exact_repository_locator_run292_2026-09-13.json").read_text(encoding="utf-8"))
    assert data["run_id"] == 292
    assert data["source"]["repository_file_name"] == "CIILP0091.pdf"
    assert data["identity_and_metadata_verification"]["first_party_repository_metadata_verified"] is True
    assert data["access_and_rights"]["pdf_bytes_acquired"] is False
    assert data["access_and_rights"]["independent_hash_verified"] is False
    assert data["access_and_rights"]["ocr_verified"] is False
    assert data["promotion"]["primary_text_promoted"] == 0
    assert data["promotion"]["controlled_claims_added"] == 0


def test_run292_has_fourteen_search_classes():
    rows = [json.loads(line) for line in Path("data/source_census/search_log_run292.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert len({row["class"] for row in rows}) == 14
