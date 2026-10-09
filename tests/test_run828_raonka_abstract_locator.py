"""Run 828: ensure exact dissertation abstract locator is auditable, not a cultural claim."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/raonka_dissertation_abstract_locator_run828_2026-10-09.json"


def test_raonka_abstract_locator_is_exact_and_bounded():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["source_id"] == "SRC-MMSC-000004"
    assert audit["evidence_id"] == "EVD-000041"
    assert "PDF page 2" in audit["exact_locator"]
    assert "ABSTRACT" in audit["exact_locator"]
    assert "May 2017" in audit["exact_locator"]
    assert "December 2018" in audit["exact_locator"]
    assert audit["release_gate"] == "NOT_PASS"
    assert "no full-text redistribution" in audit["rights"].lower()
    assert "not community validation" in audit["cultural_scope"].lower()
