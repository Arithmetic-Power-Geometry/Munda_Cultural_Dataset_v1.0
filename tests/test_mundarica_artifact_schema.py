import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "mundarica_artifact.schema.json"
REGISTRY = ROOT / "data" / "source_bundles" / "encyclopaedia_mundarica" / "artifact_registry.json"
MANIFEST = ROOT / "data" / "source_bundles" / "encyclopaedia_mundarica" / "manifest.json"


def load_schema():
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_schema_covers_all_16_volume_ids_and_separates_artifact_roles():
    schema = load_schema()
    props = schema["properties"]
    assert props["source_id"]["pattern"] == r"^SRC-MUN-V(0[1-9]|1[0-6])$"
    roles = set(props["artifact_role"]["enum"])
    assert {"authoritative_scan", "ocr_raw", "transcription_working", "transcription_verified", "structured_content"} <= roles


def test_schema_requires_provenance_rights_access_and_verification():
    schema = load_schema()
    required = set(schema["required"])
    assert {"artifact_id", "source_id", "volume", "artifact_role", "repository_path_or_locator", "rights_status", "access_class", "verification_status", "provenance"} <= required
    assert "source_description" in schema["properties"]["provenance"]["required"]


def test_schema_encodes_scan_authority_and_ocr_safety_rules():
    schema = load_schema()
    rules = json.dumps(schema["allOf"], sort_keys=True)
    assert "authoritative_scan" in rules
    assert "scan_authority" in rules
    assert "ocr_raw" in rules
    assert "verified_against_scan" in rules


def test_registry_artifacts_match_permanent_volume_ids_and_existing_paths():
    schema = load_schema()
    registry = load_registry()
    id_pattern = re.compile(schema["properties"]["artifact_id"]["pattern"])
    source_pattern = re.compile(schema["properties"]["source_id"]["pattern"])
    for artifact in registry["artifacts"]:
        assert id_pattern.fullmatch(artifact["artifact_id"])
        assert source_pattern.fullmatch(artifact["source_id"])
        assert artifact["source_id"] == f"SRC-MUN-V{artifact['volume']:02d}"
        path = artifact["repository_path_or_locator"]
        if not path.startswith(("http://", "https://")):
            assert (ROOT / path).exists(), f"registered artifact path does not exist: {path}"


def test_registry_does_not_claim_scan_authority_or_verified_text_without_evidence():
    artifacts = load_registry()["artifacts"]
    scans = [a for a in artifacts if a["artifact_role"] == "authoritative_scan"]
    assert scans == []
    for artifact in artifacts:
        if artifact["artifact_role"] in {"ocr_raw", "transcription_working"}:
            assert artifact["verification_status"] != "verified_against_scan"
            assert artifact.get("scan_authority", False) is False


def test_manifest_artifact_summary_matches_registry_and_keeps_volume_i_unverified():
    registry = load_registry()["artifacts"]
    manifest = load_manifest()
    summary = manifest["audit_summary"]
    assert manifest["artifact_registry"] == "artifact_registry.json"
    assert summary["registered_artifacts"] == len(registry)
    assert summary["registered_authoritative_scans"] == sum(a["artifact_role"] == "authoritative_scan" for a in registry)
    assert summary["registered_working_transcriptions"] == sum(a["artifact_role"] == "transcription_working" for a in registry)
    assert summary["volume_1_scan_registered"] is False
    volume_1 = next(x for x in manifest["volume_slots"] if x["volume"] == 1)
    assert volume_1["verified_complete"] is False
