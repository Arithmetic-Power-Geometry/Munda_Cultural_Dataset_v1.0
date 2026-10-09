import json
from pathlib import Path


def test_run305_barkhaa_audit():
    obj = json.loads(Path("data/source_census/ciet_ncert_barkhaa_rights_boundary_run305_2026-09-13.json").read_text(encoding="utf-8"))
    assert obj["run"] == 305
    assert obj["branch"] == "mlhkp-v2"
    assert obj["mundari_title_count"] == 9
    assert len(obj["mundari_titles"]) == 9
    assert obj["individual_audio_urls_verified"] is False
    assert obj["audio_bytes_acquired"] is False
    assert obj["reuse_rights_verified"] is False
    assert obj["content_ingested"] is False
    assert obj["claim_promotion_allowed"] is False


def test_run305_search_log_has_14_classes():
    rows = [json.loads(x) for x in Path("data/source_census/search_log_run305.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 14
    assert all(row["search_id"] == "MMSC-SEARCH-000305" for row in rows)
