import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "mundarica_volume_ix_provider_manifestation_run341_2026-09-14.json"
SEARCH = ROOT / "audits" / "mmsc_search_run341_2026-09-14.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_volume_ix_provider_metadata_does_not_become_verified_ocr_or_complete_scan():
    audit = _load(AUDIT)
    assert audit["run"] == 341
    assert audit["volume"] == "IX"
    assert audit["identifier"] == "in.ernet.dli.2015.14924"
    assert audit["provider_metadata"]["provider_totalpages"] == 346
    assert "verified complete volume" in audit["not_promoted"]
    assert "verified OCR pages" in audit["not_promoted"]
    assert audit["cultural_claims_promoted"] == 0
    assert audit["linguistic_claims_promoted"] == 0


def test_run341_census_refresh_is_14_class_and_count_neutral():
    search = _load(SEARCH)
    assert search["run"] == 341
    assert len(search["classes"]) == 14
    assert search["controlled_counts_changed"] is False
    assert search["claims_promoted"] == 0
    assert search["evidence_records_added_to_controlled_graph"] == 0


def test_homonym_and_governance_boundaries_are_explicit():
    search = _load(SEARCH)
    assert "South Sudan" in search["homonym_filter"]
    assert "Cultural access overrides entitlement" in search["governance_rule"]
