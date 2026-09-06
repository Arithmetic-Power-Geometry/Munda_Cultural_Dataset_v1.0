from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data" / "source_bundles" / "encyclopaedia_mundarica"
sys.path.insert(0, str(ROOT / "software"))
from audit_mundarica_pages import volume1_result


def load(name):
    return json.loads((BUNDLE / name).read_text(encoding="utf-8"))


def test_manifest_and_audit_cover_exactly_16_stable_volume_ids():
    manifest = load("manifest.json")
    audit = load("completeness_audit.json")
    expected = [f"SRC-MUN-V{i:02d}" for i in range(1, 17)]
    assert manifest["expected_volumes"] == 16
    assert audit["expected_volumes"] == 16
    assert [v["source_id"] for v in manifest["volume_slots"]] == expected
    assert [v["source_id"] for v in audit["volumes"]] == expected


def test_no_volume_can_claim_verified_complete_without_all_gates():
    audit = load("completeness_audit.json")
    gates = audit["policy"]["verified_complete_requires"]
    for volume in audit["volumes"]:
        if volume.get("verified_complete"):
            assert all(volume.get(gate) is True for gate in gates), volume["source_id"]


def test_manifest_verified_state_never_exceeds_audit():
    manifest = load("manifest.json")
    audit = load("completeness_audit.json")
    audited = {v["source_id"]: bool(v.get("verified_complete")) for v in audit["volumes"]}
    for slot in manifest["volume_slots"]:
        assert not slot.get("verified_complete") or audited[slot["source_id"]]


def test_manifest_public_audit_summary_matches_canonical_audit():
    manifest = load("manifest.json")
    audit = load("completeness_audit.json")
    summary = manifest["audit_summary"]
    v1 = audit["volumes"][0]
    assert summary["volume_slots"] == audit["expected_volumes"] == 16
    assert summary["verified_complete_volumes"] == sum(bool(v.get("verified_complete")) for v in audit["volumes"])
    assert summary["page_accounting_complete_volumes"] == sum(bool(v.get("page_accounting_complete")) for v in audit["volumes"])
    assert summary["volume_1_declared_scan_pages"] == v1["declared_scan_pages"]
    assert summary["volume_1_page_blocks_detected"] == v1["page_blocks_detected"]
    assert summary["volume_1_missing_page_blocks"] == v1["missing_page_blocks"]
    assert summary["volume_1_duplicate_page_blocks"] == v1["duplicate_page_blocks"]
    assert summary["volume_1_out_of_range_page_blocks"] == v1["out_of_range_page_blocks"]
    assert summary["volume_1_page_order_complete"] is v1["page_order_complete"]
    assert summary["volume_1_scan_registered"] is v1["source_scan_present"]
    note = summary["note"].lower()
    assert "structural" in note
    assert "external locator" in note and "acquired" in note
    assert "reuse permission" in note
    assert "ocr is verified" in note
    assert "verified complete" in note


def test_volume1_manifest_status_exposes_registered_accounting_without_claiming_verification():
    manifest = load("manifest.json")
    slot = manifest["volume_slots"][0]
    assert slot["source_id"] == "SRC-MUN-V01"
    assert slot["status"] == "working_transcription_registered_page_accounting_complete"
    assert slot["verified_complete"] is False


def test_volume1_working_transcription_is_not_misrepresented_as_verified():
    audit = load("completeness_audit.json")
    v1 = audit["volumes"][0]
    assert v1["repository_artifact"] == "Mundarika1.md"
    assert (ROOT / v1["repository_artifact"]).exists()
    assert v1["artifact_state"] == "working_transcription"
    assert v1["verified_complete"] is False
    assert audit["policy"]["ocr_is_not_verified_transcription"] is True


def test_volume1_has_exactly_one_ordered_page_block_for_each_declared_scan_page():
    result = volume1_result()
    assert result["declared_pages"] == 324
    assert result["page_blocks_detected"] == 324
    assert result["first_page_block"] == 1
    assert result["last_page_block"] == 324
    assert result["missing_page_blocks"] == []
    assert result["duplicate_page_blocks"] == []
    assert result["out_of_range_page_blocks"] == []
    assert result["strictly_ordered_contiguous_1_to_n"] is True
    assert result["page_accounting_complete"] is True
    assert result["certifies_scan_comparison"] is False
    assert result["certifies_transcription_accuracy"] is False
    assert result["certifies_verified_complete"] is False
