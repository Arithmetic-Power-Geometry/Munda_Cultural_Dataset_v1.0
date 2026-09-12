import json
from pathlib import Path


def test_run207_mundarica_xi_xii_pagination_boundary():
    p = Path("data/source_census/mundarica_xi_xii_bibliographic_pagination_audit_run207_2026-09-11.json")
    d = json.loads(p.read_text(encoding="utf-8"))

    assert d["run"] == 207
    assert d["work"]["title"] == "Encyclopaedia Mundarica"
    assert d["work"]["year"] == 1938
    assert d["work"]["new_permanent_source_identity_created"] is False

    e = d["secondary_bibliographic_evidence"]
    assert e["volume_XI_internal_page_range"] == "3175-3456"
    assert e["volume_XII_internal_page_range"] == "3457-3707"
    assert e["exact_digital_manifestation_acquired"] is False
    assert e["authoritative_scan_verified"] is False
    assert e["scan_page_count_verified"] is False
    assert e["ocr_verified"] is False
    assert e["transcription_verified"] is False
    assert e["verified_complete"] is False

    b = d["interpretation_boundary"]
    assert b["supports_historical_volume_identity"] is True
    assert b["supports_contiguous_internal_pagination"] is True
    assert b["supports_exact_scan_sequence"] is False
    assert b["supports_digital_file_identity"] is False
    assert b["supports_ocr_accuracy"] is False
    assert b["supports_cultural_fact_promotion"] is False
    assert b["supports_rights_or_reuse_permission"] is False
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False

    r = d["release_effect"]
    assert r["volume_XI_state_improved"] is True
    assert r["volume_XII_state_improved"] is True
    assert r["authoritative_scans_added"] == 0
    assert r["verified_complete_volumes_added"] == 0
    assert r["source_identities_added"] == 0
    assert r["claims_added"] == 0
    assert r["evidence_records_added"] == 0
    assert r["evidence_links_added"] == 0
    assert r["streamlit_modules_added"] == 0
    assert r["count_bearing_change"] is False
