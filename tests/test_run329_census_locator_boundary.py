import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "census_c16_st16_locator_run329_2026-09-14.json"
LOG = ROOT / "data" / "source_census" / "search_log_run329.jsonl"


def test_run329_census_locator_boundary_and_mmsc_refresh():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert len(data["sources"]) == 2
    assert {s["reference_id"] for s in data["sources"]} == {"PC11_C16-20", "PC11_ST16-20"}
    for source in data["sources"]:
        assert source["catalog_verified"] is True
        assert source["workbook_bytes_acquired"] is False
        assert source["independent_hash_verified"] is False
        assert source["sheet_inventory_verified"] is False
        assert source["numeric_values_promoted"] is False

    boundary = data["evidence_boundary"]
    assert boundary["source_identity_promoted_to_controlled_count"] is False
    assert boundary["numeric_evidence_promoted_to_controlled_graph_this_run"] is False
    assert boundary["cultural_claims_promoted"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_authorization_inferred"] is False

    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert len({row["class"] for row in rows}) == 14
    assert all(row["search_id"] == "MMSC-SEARCH-000329" for row in rows)
    assert not any(row["promoted"] for row in rows)
