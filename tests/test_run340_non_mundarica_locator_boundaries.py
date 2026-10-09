import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "exact_locator_records_run340_2026-09-14.json"
SEARCH = ROOT / "audits" / "mmsc_search_run340_2026-09-14.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run340_is_non_mundarica_and_count_neutral():
    audit = _load(AUDIT)
    search = _load(SEARCH)
    assert audit["run"] == 340
    assert search["run"] == 340
    assert audit["cultural_claims_promoted"] == 0
    assert audit["linguistic_claims_promoted"] == 0
    assert search["claims_promoted"] == 0
    assert search["evidence_records_added_to_controlled_graph"] == 0
    assert len(search["classes"]) == 14


def test_adibhashaa_gate_is_not_treated_as_ingested_content():
    audit = _load(AUDIT)
    rec = next(r for r in audit["records"] if r["locator_id"] == "MLHKP-LOC-R340-001")
    assert rec["mundari_manifestation"] == "data/mundari/mundari-train.csv"
    assert "gated" in rec["access_state"].lower()
    assert "exact row count" in rec["not_promoted"]
    assert "community authorization for MLHKP reuse" in rec["not_promoted"]
    assert "cultural-access authorization" in rec["not_promoted"]


def test_audio_locator_does_not_imply_consent_or_reuse_permission():
    audit = _load(AUDIT)
    audio_records = [r for r in audit["records"] if r["class"] in {"audio_datasets", "web_audio_resources"}]
    assert audio_records
    for rec in audio_records:
        joined = " ".join(rec["not_promoted"]).lower()
        assert "consent" in joined
        assert "cultural-access authorization" in rec["not_promoted"]


def test_homonym_boundary_is_explicit():
    search = _load(SEARCH)
    assert "South Sudan" in search["homonym_filter"]
