import json
from pathlib import Path


AUDIT = Path("data/source_census/mundarica_volume_v_manifestation_integrity_run268_2026-09-12.json")


def test_run268_mundarica_v_manifestation_is_not_falsely_promoted():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["identifier"] == "in.ernet.dli.2015.14925"
    assert data["identifier_ark"] == "ark:/13960/t1mh2xz66"
    assert data["repository_totalpages"] == 278
    assert data["ppi"] == 600
    assert data["page_number_confidence"] == 85
    assert data["pdf_degraded"] == "invalid-jp2-headers"
    assert data["verified_complete_volume"] is False
    assert data["authoritative_registered_scan"] is False
    assert data["ocr_verified"] is False
    assert data["printed_page_reconciliation_complete"] is False
    assert data["byte_hash_verified"] is False
    assert data["redistribution_permission_inferred"] is False
    assert data["cultural_access_permission_inferred"] is False
    assert data["community_validation_inferred"] is False


def test_run268_archive_rights_metadata_is_not_blanket_permission():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["archive_rights_metadata"] == "Out_of_copyright"
    boundary = data["rights_boundary"].lower()
    assert "not treated as blanket permission" in boundary
    assert "cultural" in boundary
