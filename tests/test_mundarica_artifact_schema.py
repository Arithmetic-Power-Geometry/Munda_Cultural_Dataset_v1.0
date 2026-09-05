import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "mundarica_artifact.schema.json"


def load_schema():
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


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
