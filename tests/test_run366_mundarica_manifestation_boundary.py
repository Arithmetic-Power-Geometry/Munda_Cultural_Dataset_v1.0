import json
from pathlib import Path


def _audit():
    path = Path("audits/mundarica_manifestation_numbering_audit_run366_2026-09-15.json")
    return json.loads(path.read_text(encoding="utf-8"))


def test_run366_does_not_promote_unverified_mundarica_claims():
    data = _audit()
    assert data["run"] == 366
    assert data["branch"] == "mlhkp-v2"
    assert data["claim_promotion"] == 0
    assert data["controlled_count_change"] is False
    assert data["mundarica_state_change"]["independently_authoritative_registered_scans"] == 0
    assert data["mundarica_state_change"]["verified_complete_volumes"] == 0
    assert data["mundarica_state_change"]["verified_ocr_pages"] == 0


def test_historical_and_commercial_numbering_are_not_equated():
    data = _audit()
    model = data["manifestation_model"]
    assert "separate manifestation lineage" in model["historical_government_printing_scheme"]
    assert "until exact content/page concordance" in model["commercial_16_volume_scheme"]
    assert "never infer" in model["canonicalization_rule"]
    assert "would not by itself prove" in model["completeness_rule"]


def test_commercial_volumes_xiv_xvi_remain_unverified():
    data = _audit()
    states = data["mundarica_state_change"]
    assert "content_mapping_unverified" in states["volume_XIV"]
    assert "content_mapping_unverified" in states["volume_XV"]
    assert "content_mapping_unverified" in states["volume_XVI"]
    assert "pagination_edition_plates_ambiguous" in states["volume_XVI"]


def test_bibliography_and_indexing_do_not_equal_ocr_or_ingestion_rights():
    data = _audit()
    for record in data["records"]:
        not_verified = set(record["does_not_verify"])
        assert "OCR completeness" in not_verified
        assert "rights for repository ingestion" in not_verified
    assert "does not count as verified OCR" in data["manifestation_model"]["ocr_rule"]
