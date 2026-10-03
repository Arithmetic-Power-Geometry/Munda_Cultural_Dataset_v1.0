import json
from pathlib import Path


def test_run188_mundarica_iv_blocked_state_is_conservative():
    p = Path("data/source_census/mundarica_volume_iv_acquisition_retry_run188_2026-09-11.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["result"] == "BLOCKED_NO_EXACT_MANIFESTATION_VERIFIED"
    assert d["exact_volume_iv_digital_manifestation_verified"] is False
    assert d["page_count_verified"] is False
    assert d["authoritative_scan_verified"] is False
    assert d["ocr_verified_as_transcription"] is False
    assert d["verified_complete"] is False
    assert d["rights_or_cultural_access_inferred"] is False
    assert d["source_identity_added"] is False
    assert d["claim_or_evidence_added"] is False
