import json
from pathlib import Path


def test_run338_locator_records():
    data = json.loads(Path("data/source_census/exact_locator_records_run338_2026-09-14.json").read_text(encoding="utf-8"))
    assert data["run"] == 338
    assert len(data["records"]) == 3
    assert data["cultural_claims_promoted"] == 0
    assert data["linguistic_claims_promoted"] == 0
    assert data["records"][0]["filename"] == "murugesanEtAl_24_Omnivoro.3.pdf"
    assert data["records"][0]["pdf_pages_observed"] == 48
    assert data["records"][1]["declared_file"] == "CIILP0091.pdf"
    assert data["records"][2]["declared_file"] == "BVP04859.pdf"


def test_run338_search_log_counts():
    log = json.loads(Path("audits/mmsc_search_run338_2026-09-14.json").read_text(encoding="utf-8"))
    assert len(log["classes"]) == 14
    assert log["controlled_counts"]["audited_source_identities"] == 42
    assert log["controlled_counts"]["unresolved_unique_web_leads"] == 73
    assert log["false_completeness_claimed"] is False
