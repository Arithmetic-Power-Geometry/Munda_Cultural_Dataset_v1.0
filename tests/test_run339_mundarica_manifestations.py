import json
from pathlib import Path


def test_run339_mundarica_provider_manifestations_preserve_verification_boundary():
    data = json.loads(Path("data/source_census/mundarica_provider_manifestations_run339_2026-09-14.json").read_text(encoding="utf-8"))
    assert data["run"] == 339
    assert len(data["records"]) == 2
    assert data["aggregate_controlled_state"]["authoritative_registered_scans"] == 0
    assert data["aggregate_controlled_state"]["verified_complete_volumes"] == 0
    assert data["aggregate_controlled_state"]["verified_ocr_pages"] == 0
    assert data["records"][0]["volume"] == "X"
    assert data["records"][0]["identifier"] == "dli.bengal.10689.20997"
    assert data["records"][0]["provider_totalpages"] == 288
    assert data["records"][0]["counts_as_verified_ocr_pages"] == 0
    assert data["records"][1]["volume"] == "XIII"
    assert data["records"][1]["identifier"] == "dli.ernet.14932"
    assert data["false_ocr_verification_claimed"] is False
    assert data["cultural_claims_promoted"] == 0


def test_run339_mmsc_controlled_counts_unchanged_without_reconciliation():
    log = json.loads(Path("audits/mmsc_search_run339_2026-09-14.json").read_text(encoding="utf-8"))
    assert len(log["classes"]) == 14
    assert log["controlled_counts"]["audited_source_identities"] == 42
    assert log["controlled_counts"]["canonicalized_unique_web_leads"] == 14
    assert log["controlled_counts"]["unresolved_unique_web_leads"] == 73
    assert log["false_completeness_claimed"] is False
