import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "source_census" / "bangladesh_multiling_ciil_grammar_exact_locator_run350_2026-09-14.json"


def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def test_run350_is_locator_only_and_does_not_promote_claims():
    data = load_record()
    assert data["run"] == 350
    assert data["controlled_claims_promoted"] == 0
    assert data["controlled_evidence_records_promoted"] == 0
    assert data["controlled_counts_changed"] is False
    assert all(r["promotion_level"].endswith("metadata_only") for r in data["records"])


def test_multiling_rights_and_consent_boundaries_are_explicit():
    data = load_record()
    rec = next(r for r in data["records"] if r["source_key"] == "BANGLADESH-MULTILING-MUNDA")
    assert rec["rights_access_consents"]["reuse_permission_inferred"] is False
    assert rec["rights_access_consents"]["participant_consent_verified"] is False
    assert rec["rights_access_consents"]["community_validation_verified"] is False
    assert rec["rights_access_consents"]["cultural_access_authorized"] is False
    assert "individual audio files" in rec["not_promoted"]


def test_ciil_manifestation_is_not_treated_as_materialized_content():
    data = load_record()
    rec = next(r for r in data["records"] if r["source_key"] == "CIIL-RAMDAYAL-MUNDA-MUNDARI-VYAKARAN-2013")
    assert rec["declared_file"] == "BVP00202.pdf"
    assert "PDF bytes" in rec["not_promoted"]
    assert "independent cryptographic hash" in rec["not_promoted"]
    assert "grammatical claims" in rec["not_promoted"]
    assert rec["rights_access_consents"]["reuse_permission_verified"] is False
