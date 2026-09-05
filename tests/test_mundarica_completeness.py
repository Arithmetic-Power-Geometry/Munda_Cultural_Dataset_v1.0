from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data" / "source_bundles" / "encyclopaedia_mundarica"


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


def test_volume1_working_transcription_is_not_misrepresented_as_verified():
    audit = load("completeness_audit.json")
    v1 = audit["volumes"][0]
    assert v1["repository_artifact"] == "Mundarika1.md"
    assert (ROOT / v1["repository_artifact"]).exists()
    assert v1["artifact_state"] == "working_transcription"
    assert v1["verified_complete"] is False
    assert audit["policy"]["ocr_is_not_verified_transcription"] is True
