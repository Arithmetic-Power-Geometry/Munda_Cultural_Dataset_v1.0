import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_stage2_validator_passes():
    result = subprocess.run(
        [sys.executable, str(ROOT / "software" / "validate_master_source_register.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "MLHKP MASTER SOURCE REGISTER: PASS" in result.stdout


def test_all_legacy_ids_preserved_exactly():
    with (ROOT / "data" / "sources.csv").open("r", encoding="utf-8-sig", newline="") as f:
        legacy = {r["source_id"] for r in csv.DictReader(f)}
    register = json.loads((ROOT / "data" / "source_register" / "master_sources.json").read_text(encoding="utf-8"))
    migrated = {r["source_id"] for r in register["sources"]}
    assert legacy == migrated
    assert len(legacy) == 14


def test_mundarica_slots_are_complete_and_noncolliding():
    register = json.loads((ROOT / "data" / "source_register" / "master_sources.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "data" / "source_bundles" / "encyclopaedia_mundarica" / "manifest.json").read_text(encoding="utf-8"))
    registered = {r["source_id"] for r in register["sources"]}
    slots = [r["source_id"] for r in manifest["volume_slots"]]
    assert slots == [f"SRC-MUN-V{i:02d}" for i in range(1, 17)]
    assert not (registered & set(slots))


def test_future_source_schema_is_extensible():
    schema = json.loads((ROOT / "schemas" / "source_record.schema.json").read_text(encoding="utf-8"))
    # Future source types are strings rather than a closed enum; extensibility is deliberate.
    assert schema["properties"]["source_type"]["type"] == "string"
    assert "extended_data" in schema["properties"]
    assert "locators" in schema["properties"]
    assert "identifiers" in schema["properties"]
