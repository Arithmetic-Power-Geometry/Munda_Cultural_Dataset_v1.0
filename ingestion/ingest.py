#!/usr/bin/env python3
"""MLHKP universal JSON ingestion engine.

Drop JSON bundles into imports/pending/ and run this script. The engine validates
minimum envelope fields, prevents duplicate permanent IDs within a bundle and
against the current registry, routes accepted bundles by source type, rebuilds
the registry index and emits an auditable import report.

This script deliberately does NOT convert source passages into established
cultural facts. Semantic review remains a separate scholarly step.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / "imports" / "pending"
DATA_ROOT = ROOT / "data" / "source_bundles"
REGISTRY_DIR = ROOT / "data" / "registry"
REGISTRY_FILE = REGISTRY_DIR / "import_index.json"
REPORT_DIR = ROOT / "imports" / "reports"

RECORD_TYPES = {
    "source_bundle",
    "field_bundle",
    "media_metadata",
    "entity_bundle",
    "evidence_bundle",
}

ACCESS_CLASSES = {
    "open",
    "community_access_only",
    "research_restricted",
    "embargoed",
    "confidential",
    "not_for_publication",
}

SOURCE_ROUTE = {
    "encyclopaedia": "encyclopaedia",
    "book": "books",
    "journal_article": "journals",
    "thesis": "theses",
    "government_source": "government",
    "archive": "archives",
    "newspaper": "newspapers",
    "website": "websites",
    "dictionary": "dictionaries",
    "interview": "fieldwork/interviews",
    "oral_history": "fieldwork/oral_histories",
    "observation": "fieldwork/observations",
    "event": "fieldwork/events",
    "field_note": "fieldwork/field_notes",
    "community_validation": "fieldwork/community_validations",
    "photograph": "media_metadata/photographs",
    "audio": "media_metadata/audio",
    "video": "media_metadata/video",
    "object": "entities/objects",
    "map": "media_metadata/maps",
    "other": "other",
}

ID_KEYS = {
    "source_id",
    "entry_id",
    "passage_id",
    "claim_id",
    "evidence_id",
    "term_id",
    "object_id",
    "place_id",
    "event_id",
    "step_id",
    "interview_id",
    "segment_id",
    "media_id",
    "validation_id",
    "variation_id",
    "contradiction_id",
    "discovery_id",
    "relationship_id",
    "indicator_id",
    "domain_id",
    "subdomain_id",
    "book_claim_id",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def walk_ids(obj: Any) -> Iterable[tuple[str, str]]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in ID_KEYS and isinstance(value, str) and value.strip():
                yield key, value.strip()
            yield from walk_ids(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_ids(item)


def validate_bundle(bundle: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(bundle, dict):
        return ["Top-level JSON value must be an object."]

    for key in ("mcd_schema", "record_type", "source_type", "source"):
        if key not in bundle:
            errors.append(f"Missing required field: {key}")

    if bundle.get("record_type") not in RECORD_TYPES:
        errors.append(f"Unsupported record_type: {bundle.get('record_type')!r}")

    source = bundle.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        if not source.get("source_id"):
            errors.append("source.source_id is required")
        if not source.get("title"):
            errors.append("source.title is required")
        access = source.get("access_class", "open")
        if access not in ACCESS_CLASSES:
            errors.append(f"Invalid source.access_class: {access!r}")

    ids = list(walk_ids(bundle))
    seen: dict[str, str] = {}
    for key, value in ids:
        if value in seen:
            errors.append(
                f"Duplicate permanent ID inside bundle: {value} "
                f"({seen[value]} and {key})"
            )
        else:
            seen[value] = key

    # Special safety rule for historical OCR corpora.
    if bundle.get("source_type") == "encyclopaedia":
        def inspect(node: Any) -> None:
            if isinstance(node, dict):
                status = node.get("verification_status")
                if status == "verified_against_scan" and not node.get("transcription") and not node.get("transcription_corrected"):
                    errors.append(
                        "A record marked verified_against_scan must contain a verified transcription."
                    )
                for v in node.values():
                    inspect(v)
            elif isinstance(node, list):
                for v in node:
                    inspect(v)
        inspect(bundle)

    return errors


def load_registry() -> dict[str, Any]:
    if REGISTRY_FILE.exists():
        reg = load_json(REGISTRY_FILE)
        if isinstance(reg, dict):
            return reg
    return {
        "schema": "MLHKP_IMPORT_INDEX_1.0",
        "updated_utc": None,
        "bundles": [],
        "permanent_ids": {},
    }


def safe_name(source_id: str, filename: str) -> str:
    stem = Path(filename).stem
    return f"{source_id}__{stem}.json"


def route_for(bundle: dict[str, Any]) -> Path:
    source_type = str(bundle.get("source_type", "other"))
    route = SOURCE_ROUTE.get(source_type, "other")

    # Give Encyclopaedia Mundarica a stable first-class corpus path.
    source = bundle.get("source", {})
    collection_id = source.get("collection_id")
    title = str(source.get("title", "")).lower()
    if source_type == "encyclopaedia" and (
        collection_id == "SRC-COL-MUNDARICA" or "mundarica" in title
    ):
        route = "encyclopaedia_mundarica"

    return DATA_ROOT / route


def process_file(path: Path, registry: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
    raw = path.read_bytes()
    result: dict[str, Any] = {
        "input_file": str(path.relative_to(ROOT)),
        "sha256": sha256_bytes(raw),
        "status": "rejected",
        "errors": [],
        "destination": None,
    }

    try:
        bundle = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        result["errors"] = [f"Invalid UTF-8 JSON: {exc}"]
        return result

    errors = validate_bundle(bundle)
    if errors:
        result["errors"] = errors
        return result

    source = bundle["source"]
    source_id = source["source_id"]
    new_ids = dict(walk_ids(bundle))
    registry_ids: dict[str, Any] = registry.setdefault("permanent_ids", {})

    collisions = []
    for _, pid in walk_ids(bundle):
        if pid in registry_ids:
            collisions.append(
                f"Permanent ID already registered: {pid} -> {registry_ids[pid]}"
            )
    if collisions:
        result["errors"] = collisions
        return result

    destination_dir = route_for(bundle)
    destination = destination_dir / safe_name(source_id, path.name)
    result["destination"] = str(destination.relative_to(ROOT))

    if not dry_run:
        destination_dir.mkdir(parents=True, exist_ok=True)
        # Canonical pretty JSON for reproducible diffs.
        dump_json(destination, bundle)

        for key, pid in walk_ids(bundle):
            registry_ids[pid] = {
                "kind": key,
                "bundle": str(destination.relative_to(ROOT)),
                "source_id": source_id,
            }

        registry.setdefault("bundles", []).append({
            "source_id": source_id,
            "title": source.get("title"),
            "source_type": bundle.get("source_type"),
            "record_type": bundle.get("record_type"),
            "access_class": source.get("access_class", "open"),
            "path": str(destination.relative_to(ROOT)),
            "sha256": result["sha256"],
            "ingested_utc": utc_now(),
        })

        # Remove accepted staging file only after canonical copy succeeds.
        path.unlink()

    result["status"] = "accepted"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=str(PENDING))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.path)
    if not input_path.is_absolute():
        input_path = (ROOT / input_path).resolve()

    if input_path.is_file():
        files = [input_path]
    else:
        input_path.mkdir(parents=True, exist_ok=True)
        files = sorted(input_path.rglob("*.json"))

    registry = load_registry()
    results = []
    for path in files:
        results.append(process_file(path, registry, dry_run=args.dry_run))

    accepted = sum(r["status"] == "accepted" for r in results)
    rejected = len(results) - accepted

    report = {
        "schema": "MLHKP_IMPORT_REPORT_1.0",
        "generated_utc": utc_now(),
        "dry_run": args.dry_run,
        "files_seen": len(results),
        "accepted": accepted,
        "rejected": rejected,
        "results": results,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "latest_import_report.json"
    dump_json(report_path, report)

    if not args.dry_run:
        registry["updated_utc"] = utc_now()
        registry["bundle_count"] = len(registry.get("bundles", []))
        registry["permanent_id_count"] = len(registry.get("permanent_ids", {}))
        dump_json(REGISTRY_FILE, registry)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
