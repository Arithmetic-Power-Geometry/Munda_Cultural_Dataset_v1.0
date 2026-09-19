import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCATOR = ROOT / "data/source_census/wals_phoible_mundari_exact_locator_run349_2026-09-14.json"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run349_locator_boundary():
    data = json.loads(LOCATOR.read_text(encoding="utf-8"))
    assert data["run"] == 349
    assert data["controlled_claims_added"] == 0
    assert data["controlled_evidence_records_added"] == 0
    assert data["controlled_counts_changed"] is False
    assert len(data["records"]) == 2
    providers = {r["provider"] for r in data["records"]}
    assert providers == {"WALS Online", "PHOIBLE 2.0"}
    for record in data["records"]:
        assert "community validation" in record["not_promoted"]
        assert "cultural-access authorization" in record["not_promoted"]


def test_run349_no_controlled_count_inflation():
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["mmsc"]["audited_source_identities"] == 42
    assert status["mmsc"]["raw_web_discovery_records"] == 90
    assert status["mmsc"]["unique_web_discovery_leads"] == 87
    assert status["mmsc"]["canonicalized_unique_web_leads"] == 14
    assert status["mmsc"]["unresolved_unique_web_leads"] == 73
    assert status["evidence"]["claims"] == 52
    assert status["evidence"]["records"] == 52
    assert status["evidence"]["links"] == 52
