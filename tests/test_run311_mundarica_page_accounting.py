import json
from pathlib import Path


def test_run311_mundarica_page_accounting_boundary():
    path = Path("data/source_census/mundarica_historical_page_accounting_run311_2026-09-13.json")
    obj = json.loads(path.read_text(encoding="utf-8"))

    assert obj["run"] == 311
    findings = obj["findings"]
    assert any(x["volumes"] == "I-IV" and x["reported_pagination"] == "v + 1271" for x in findings)
    assert any(x["volumes"] == "VIII-X" and x["reported_pagination"] == "2147-3173" for x in findings)

    verification = obj["verification"]
    assert verification["bibliographic_identity_verified"] is True
    assert verification["historical_printed_page_ranges_supported"] is True
    assert verification["per_volume_split_inferred"] is False
    assert verification["primary_scan_bytes_acquired"] is False
    assert verification["scan_image_page_concordance_verified"] is False
    assert verification["ocr_verified"] is False
    assert verification["complete_volume_verified"] is False

    promotion = obj["evidence_promotion"]
    assert promotion["new_controlled_cultural_claims"] == 0
    assert promotion["new_evidence_records"] == 0
    assert promotion["new_provenance_links"] == 0
    assert promotion["count_neutral"] is True
