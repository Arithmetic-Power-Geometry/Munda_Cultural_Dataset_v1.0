import json
from pathlib import Path


def test_run205_mundarica_volume_ix_secondary_locator_boundary():
    p = Path("data/source_census/mundarica_volume_ix_secondary_page_locator_run205_2026-09-11.json")
    d = json.loads(p.read_text(encoding="utf-8"))

    assert d["run"] == 205
    assert d["work"]["volume"] == "IX"
    assert d["work"]["manifestation_verified_this_run"] is False
    assert d["work"]["authoritative_scan_verified"] is False
    assert d["work"]["ocr_verified"] is False
    assert d["work"]["transcription_verified"] is False
    assert d["work"]["verified_complete"] is False

    pages = [x["page"] for x in d["reported_internal_locators"]]
    assert pages == [2756, 2881]
    assert all(x["content_promoted"] is False for x in d["reported_internal_locators"])

    b = d["verification_boundary"]
    assert b["cultural_content_ingested"] is False
    assert b["claims_added"] == 0
    assert b["evidence_records_added"] == 0
    assert b["source_identities_added"] == 0
    assert b["count_bearing_change"] is False

    r = d["release_effect"]
    assert r["volume_ix_locator_state_strengthened"] is True
    assert r["volume_ix_manifestation_state_changed"] is False
    assert r["authoritative_scans_registered_delta"] == 0
    assert r["verified_complete_volumes_delta"] == 0
