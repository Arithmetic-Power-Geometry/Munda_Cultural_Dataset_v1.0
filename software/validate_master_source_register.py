#!/usr/bin/env python3
"""Validate the MLHKP Master Source Register and prove lossless migration of MCD v1 sources."""
from __future__ import annotations

import copy
import csv
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "data" / "sources.csv"
REGISTER = ROOT / "data" / "source_register" / "master_sources.json"
REGISTER_SCHEMA = ROOT / "schemas" / "master_source_register.schema.json"
SOURCE_SCHEMA = ROOT / "schemas" / "source_record.schema.json"
MUNDARICA_MANIFEST = ROOT / "data" / "source_bundles" / "encyclopaedia_mundarica" / "manifest.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Cannot read valid JSON from {path}: {exc}")


def normalize_year(value) -> str:
    return str(value).strip()


def schema_error_text(errors) -> str:
    rendered = []
    for error in errors[:10]:
        path = ".".join(str(part) for part in error.absolute_path) or "<root>"
        rendered.append(f"{path}: {error.message}")
    return " | ".join(rendered)


def main() -> None:
    for path in [LEGACY, REGISTER, REGISTER_SCHEMA, SOURCE_SCHEMA, MUNDARICA_MANIFEST]:
        if not path.exists():
            fail(f"Required file missing: {path.relative_to(ROOT)}")

    register = load_json(REGISTER)
    register_schema = load_json(REGISTER_SCHEMA)
    source_schema = load_json(SOURCE_SCHEMA)
    manifest = load_json(MUNDARICA_MANIFEST)

    Draft202012Validator.check_schema(source_schema)
    Draft202012Validator.check_schema(register_schema)

    # Keep the public register schema modular, but resolve its source-record schema
    # locally for offline/reproducible validation. This deliberately avoids network
    # resolution of the schema $id and makes CI deterministic.
    local_register_schema = copy.deepcopy(register_schema)
    local_register_schema["properties"]["sources"]["items"] = source_schema
    register_errors = sorted(
        Draft202012Validator(local_register_schema).iter_errors(register),
        key=lambda e: list(e.absolute_path),
    )
    if register_errors:
        fail("Register schema validation failed: " + schema_error_text(register_errors))

    source_validator = Draft202012Validator(source_schema)
    for index, source in enumerate(register.get("sources", [])):
        errors = sorted(source_validator.iter_errors(source), key=lambda e: list(e.absolute_path))
        if errors:
            fail(f"Source record {index} schema validation failed: " + schema_error_text(errors))

    sources = register["sources"]
    ids = [s["source_id"] for s in sources]
    if len(ids) != len(set(ids)):
        fail("Duplicate source_id found in master register")
    if register.get("source_count") != len(sources):
        fail("source_count does not equal actual source array length")

    with LEGACY.open("r", encoding="utf-8-sig", newline="") as handle:
        legacy_rows = list(csv.DictReader(handle))

    legacy_ids = [r["source_id"].strip() for r in legacy_rows]
    if len(legacy_ids) != len(set(legacy_ids)):
        fail("Duplicate source_id found in legacy sources.csv")
    if register.get("legacy_source_count") != len(legacy_rows):
        fail("legacy_source_count does not equal sources.csv row count")

    current = {s["source_id"]: s for s in sources}
    if set(legacy_ids) != set(current):
        missing = sorted(set(legacy_ids) - set(current))
        extra = sorted(set(current) - set(legacy_ids))
        fail(f"Lossless migration check failed; missing={missing}, extra={extra}")

    fields = ["source_class", "title", "creator", "source_type", "geographic_scope", "scope_note"]
    for row in legacy_rows:
        sid = row["source_id"].strip()
        rec = current[sid]
        for field in fields:
            legacy_value = (row.get(field) or "").strip()
            new_value = str(rec.get(field) or "").strip()
            if legacy_value != new_value:
                fail(f"{sid}: field {field!r} changed during migration: {legacy_value!r} != {new_value!r}")

        if normalize_year(row.get("year")) != normalize_year(rec.get("year")):
            fail(f"{sid}: year changed during migration: {row.get('year')!r} != {rec.get('year')!r}")

        legacy_url = (row.get("url") or "").strip()
        primary = [x["value"] for x in rec.get("locators", []) if x.get("is_primary")]
        if legacy_url and legacy_url not in primary:
            fail(f"{sid}: legacy URL was not preserved as a primary locator")

        reuse = (row.get("reuse_note") or "").strip()
        if reuse != str(rec.get("reuse_status") or "").strip():
            fail(f"{sid}: legacy reuse_note was not preserved")

    # Universal-register quality gates.
    for rec in sources:
        if not rec.get("language"):
            fail(f"{rec['source_id']}: at least one language is required")
        if not rec.get("locators"):
            fail(f"{rec['source_id']}: at least one locator is required")
        if not any(x.get("is_primary") for x in rec["locators"]):
            fail(f"{rec['source_id']}: at least one primary locator is required")
        if "legacy" not in rec or rec["legacy"].get("source_id") != rec["source_id"]:
            fail(f"{rec['source_id']}: legacy source identity is not explicitly preserved")

    # Ensure the future 16-volume Mundarica collection is addressable without ID collisions.
    slots = manifest.get("volume_slots", [])
    if manifest.get("expected_volumes") != 16 or len(slots) != 16:
        fail("Encyclopaedia Mundarica manifest must reserve exactly 16 volume slots")
    slot_ids = [x.get("source_id") for x in slots]
    expected_slot_ids = [f"SRC-MUN-V{i:02d}" for i in range(1, 17)]
    if slot_ids != expected_slot_ids:
        fail("Mundarica volume source IDs are not exactly SRC-MUN-V01 through SRC-MUN-V16")
    if set(slot_ids) & set(ids):
        fail("Reserved Mundarica volume IDs collide with legacy source IDs")

    print("MLHKP MASTER SOURCE REGISTER: PASS")
    print(f"Legacy sources preserved: {len(legacy_rows)}/{len(legacy_rows)}")
    print(f"Registered sources: {len(sources)}")
    print("Duplicate source IDs: 0")
    print("Legacy IDs lost: 0")
    print("Legacy core fields changed: 0")
    print("Mundarica volume slots reserved: 16/16")
    print("Universal source schema: valid Draft 2020-12")
    print("Register schema: valid Draft 2020-12")


if __name__ == "__main__":
    main()
