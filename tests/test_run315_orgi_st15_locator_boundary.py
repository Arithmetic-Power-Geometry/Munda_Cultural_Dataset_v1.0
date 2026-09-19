import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/orgi_st15_jharkhand_locator_audit_run315_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run315.jsonl"


def test_orgi_st15_locator_boundary():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["run"] == 315
    assert d["source"]["reference_id"] == "PC11_ST15-20"
    assert d["source"]["declared_download_filename"] == "ST-20-00-15-DDW-2011.XLSX"
    q = d["quality_boundary"]
    assert q["workbook_bytes_independently_acquired"] is False
    assert q["independent_hash_computed"] is False
    assert q["sheet_inventory_verified"] is False
    assert q["numeric_cells_verified"] is False
    assert q["mundari_or_munda_rows_verified_from_workbook"] is False
    assert q["controlled_evidence_records_added"] == 0
    assert q["claims_promoted"] == 0
    g = d["rights_governance_boundary"]
    assert g["cultural_access_overrides_entitlement"] is True
    assert g["public_access_treated_as_reuse_permission"] is False
    assert g["participant_consent_inferred"] is False
    assert g["community_validation_inferred"] is False
    assert g["cultural_access_authorization_inferred"] is False


def test_run315_search_log_covers_all_controlled_classes():
    rows = [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 14
    assert len({r["class"] for r in rows}) == 14
    assert all(r["run"] == 315 for r in rows)
