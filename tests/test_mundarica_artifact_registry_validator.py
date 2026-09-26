import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "software" / "validate_mundarica_artifact_registry.py"
REGISTRY_PATH = ROOT / "data" / "source_bundles" / "encyclopaedia_mundarica" / "artifact_registry.json"

spec = importlib.util.spec_from_file_location("mundarica_registry_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def registry():
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_current_registry_passes_validator_without_claiming_verification():
    result = validator.validate_registry(registry())
    assert result["ok"] is True
    assert result["artifact_count"] == 1
    assert result["role_counts"]["transcription_working"] == 1
    assert result["role_counts"]["authoritative_scan"] == 0
    assert result["errors"] == []


def test_rejects_source_volume_identity_mismatch():
    mutated = copy.deepcopy(registry())
    mutated["artifacts"][0]["volume"] = 2
    result = validator.validate_registry(mutated)
    assert result["ok"] is False
    assert any("source_id/volume mismatch" in error for error in result["errors"])


def test_rejects_working_transcription_as_verified_against_scan():
    mutated = copy.deepcopy(registry())
    mutated["artifacts"][0]["verification_status"] = "verified_against_scan"
    result = validator.validate_registry(mutated)
    assert result["ok"] is False
    assert any("transcription_working cannot be marked verified_against_scan" in error for error in result["errors"])


def test_rejects_scan_authority_on_non_scan_artifact():
    mutated = copy.deepcopy(registry())
    mutated["artifacts"][0]["scan_authority"] = True
    result = validator.validate_registry(mutated)
    assert result["ok"] is False
    assert any("non-scan artifact cannot claim scan_authority=true" in error for error in result["errors"])


def test_rejects_missing_repository_artifact():
    mutated = copy.deepcopy(registry())
    mutated["artifacts"][0]["repository_path_or_locator"] = "data/source_bundles/encyclopaedia_mundarica/DOES_NOT_EXIST.txt"
    result = validator.validate_registry(mutated)
    assert result["ok"] is False
    assert any("registered repository file does not exist" in error for error in result["errors"])


def test_warns_but_does_not_infer_reuse_rights_from_open_access():
    result = validator.validate_registry(registry())
    assert result["ok"] is True
    assert any("access does not imply reuse permission" in warning for warning in result["warnings"])
