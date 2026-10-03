import json
from pathlib import Path


def test_run304_barkhaa_locator():
    p = Path("data/source_census/ciet_ncert_barkhaa_locator_run304_2026-09-13.json")
    obj = json.loads(p.read_text(encoding="utf-8"))
    assert obj["run"] == 304
    assert obj["branch"] == "mlhkp-v2"
    assert obj["count"] == 9
    assert len(obj["mundari_titles"]) == 9
    assert obj["content_ingested"] is False
    assert obj["rights_verified"] is False
    assert obj["counts_changed"] is False


def test_run304_search_log_has_14_classes():
    rows = [json.loads(x) for x in Path("data/source_census/search_log_run304.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 14
    assert all(row["search_id"] == "MMSC-SEARCH-000304" for row in rows)
