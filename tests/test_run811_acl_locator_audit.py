"""Run 811: exact-locator, scope and controlled-count guard for ACL paper."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/acl_kamau_2025_mmloso_mt_exact_locator_run811_2026-10-08.json"

def _audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))

def test_run811_exact_locator_audit():
    audit = _audit()
    assert audit["branch"] == "mlhkp-v2"
    assert audit["source"]["canonical_key"] == "ACL:2025.mmloso-1.11"
    assert audit["source"]["pages"] == "106-108"
    assert len(audit["exact_locator_candidates"]) == 6
    assert all("printed p." in x["locator"] and "PDF p." in x["locator"] for x in audit["exact_locator_candidates"])
    assert all(x["boundary"] for x in audit["exact_locator_candidates"])

def test_run811_no_unsupported_promotion():
    audit = _audit()
    assert audit["identity_reconciliation"]["required"] is True
    assert audit["identity_reconciliation"]["count_new_identity"] == 0
    assert set(audit["controlled_delta"].values()) == {0}
    assert audit["rights_governance"]["translation_examples_redistributed"] is False
    assert audit["rights_governance"]["cultural_knowledge_claims_promoted"] is False
    assert audit["release_gate"] == "NOT_PASS"

def test_run811_multilingual_scores_not_mundari_specific():
    audit = _audit()
    table = next(x for x in audit["exact_locator_candidates"] if "Table 1" in x["locator"])
    assert "Mundari-only" in table["boundary"]
    assert "179.49" in table["proposition"]
