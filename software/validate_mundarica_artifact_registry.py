#!/usr/bin/env python3
"""Deterministically validate the MLHKP Encyclopaedia Mundarica artifact registry.

This validator checks metadata, repository presence, permanent source/volume identity,
rights/access declarations, and forbidden verification-state combinations. It does
not assess transcription accuracy, cultural meaning, scan authenticity, or rights.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "source_bundles" / "encyclopaedia_mundarica" / "artifact_registry.json"
SCHEMA_PATH = ROOT / "schemas" / "mundarica_artifact.schema.json"

ARTIFACT_ID_RE = re.compile(r"^SRC-MUN-V(0[1-9]|1[0-6])-ART-[A-Z0-9_-]+$")
SOURCE_ID_RE = re.compile(r"^SRC-MUN-V(0[1-9]|1[0-6])$")
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")

ALLOWED_ROLES = {
    "authoritative_scan",
    "ocr_raw",
    "transcription_working",
    "transcription_verified",
    "structured_content",
    "page_image",
    "index_or_appendix",
    "other",
}
ALLOWED_RIGHTS = {
    "checked_reusable",
    "checked_link_only",
    "permission_required",
    "rights_unclear",
    "restricted",
    "not_assessed",
}
ALLOWED_ACCESS = {
    "open",
    "community_access_only",
    "research_restricted",
    "embargoed",
    "confidential",
    "not_for_publication",
}
ALLOWED_VERIFICATION = {
    "unverified",
    "structurally_audited",
    "verified_against_scan",
    "requires_specialist_review",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_remote_locator(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_registry(registry: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if registry.get("record_type") != "mundarica_artifact_registry":
        errors.append("record_type must be 'mundarica_artifact_registry'")
    if registry.get("collection_id") != "SRC-COL-MUNDARICA":
        errors.append("collection_id must be 'SRC-COL-MUNDARICA'")
    if registry.get("schema") != "schemas/mundarica_artifact.schema.json":
        errors.append("registry schema path must remain schemas/mundarica_artifact.schema.json")

    artifacts = registry.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("artifacts must be a list")
        artifacts = []

    seen_artifact_ids: set[str] = set()
    role_counts: dict[str, int] = {role: 0 for role in sorted(ALLOWED_ROLES)}
    source_counts: dict[str, int] = {}

    required = {
        "artifact_id",
        "source_id",
        "volume",
        "artifact_role",
        "repository_path_or_locator",
        "rights_status",
        "access_class",
        "verification_status",
        "provenance",
    }

    for index, artifact in enumerate(artifacts):
        prefix = f"artifact[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{prefix} must be an object")
            continue

        missing = sorted(required - set(artifact))
        if missing:
            errors.append(f"{prefix} missing required fields: {', '.join(missing)}")
            continue

        artifact_id = artifact["artifact_id"]
        source_id = artifact["source_id"]
        volume = artifact["volume"]
        role = artifact["artifact_role"]
        locator = artifact["repository_path_or_locator"]
        rights = artifact["rights_status"]
        access = artifact["access_class"]
        verification = artifact["verification_status"]
        provenance = artifact["provenance"]
        scan_authority = artifact.get("scan_authority", False)

        if not isinstance(artifact_id, str) or not ARTIFACT_ID_RE.fullmatch(artifact_id):
            errors.append(f"{prefix} invalid artifact_id: {artifact_id!r}")
        elif artifact_id in seen_artifact_ids:
            errors.append(f"{prefix} duplicate artifact_id: {artifact_id}")
        else:
            seen_artifact_ids.add(artifact_id)

        if not isinstance(source_id, str) or not SOURCE_ID_RE.fullmatch(source_id):
            errors.append(f"{prefix} invalid source_id: {source_id!r}")
        if not isinstance(volume, int) or isinstance(volume, bool) or not 1 <= volume <= 16:
            errors.append(f"{prefix} volume must be integer 1..16")
        elif source_id != f"SRC-MUN-V{volume:02d}":
            errors.append(f"{prefix} source_id/volume mismatch: {source_id} vs volume {volume}")

        if role not in ALLOWED_ROLES:
            errors.append(f"{prefix} invalid artifact_role: {role!r}")
        else:
            role_counts[role] += 1
        if rights not in ALLOWED_RIGHTS:
            errors.append(f"{prefix} invalid rights_status: {rights!r}")
        if access not in ALLOWED_ACCESS:
            errors.append(f"{prefix} invalid access_class: {access!r}")
        if verification not in ALLOWED_VERIFICATION:
            errors.append(f"{prefix} invalid verification_status: {verification!r}")

        if not isinstance(provenance, dict) or not str(provenance.get("source_description", "")).strip():
            errors.append(f"{prefix} provenance.source_description is required")

        if not isinstance(locator, str) or not locator.strip():
            errors.append(f"{prefix} repository_path_or_locator must be non-empty")
        elif is_remote_locator(locator):
            warnings.append(f"{prefix} uses remote locator; repository byte-presence cannot be checked")
        else:
            candidate = (ROOT / locator).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{prefix} repository path escapes repository root: {locator}")
            else:
                if not candidate.is_file():
                    errors.append(f"{prefix} registered repository file does not exist: {locator}")
                else:
                    registered_sha = artifact.get("sha256")
                    if registered_sha is not None:
                        if not isinstance(registered_sha, str) or not SHA256_RE.fullmatch(registered_sha):
                            errors.append(f"{prefix} sha256 must be 64 hexadecimal characters or null")
                        else:
                            actual_sha = sha256_file(candidate)
                            if actual_sha.lower() != registered_sha.lower():
                                errors.append(f"{prefix} sha256 mismatch for {locator}")

        if role == "authoritative_scan" and scan_authority is not True:
            errors.append(f"{prefix} authoritative_scan requires scan_authority=true")
        if role != "authoritative_scan" and scan_authority is True:
            errors.append(f"{prefix} non-scan artifact cannot claim scan_authority=true")
        if role in {"ocr_raw", "transcription_working"} and verification == "verified_against_scan":
            errors.append(f"{prefix} {role} cannot be marked verified_against_scan")
        if role == "transcription_verified" and verification != "verified_against_scan":
            errors.append(f"{prefix} transcription_verified requires verification_status=verified_against_scan")

        if rights in {"restricted", "permission_required", "rights_unclear", "not_assessed"} and access == "open":
            warnings.append(
                f"{prefix} is open-access while rights_status={rights}; access does not imply reuse permission"
            )

        if isinstance(source_id, str):
            source_counts[source_id] = source_counts.get(source_id, 0) + 1

    return {
        "ok": not errors,
        "registry": str(REGISTRY_PATH.relative_to(ROOT)),
        "schema_present": SCHEMA_PATH.is_file(),
        "artifact_count": len(artifacts),
        "source_ids_with_artifacts": sorted(source_counts),
        "role_counts": role_counts,
        "errors": errors,
        "warnings": warnings,
        "policy_note": "Structural registry validation does not establish cultural accuracy, scan authenticity, transcription verification, or reuse rights.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    if not REGISTRY_PATH.is_file():
        result = {"ok": False, "errors": [f"missing registry: {REGISTRY_PATH.relative_to(ROOT)}"]}
    elif not SCHEMA_PATH.is_file():
        result = {"ok": False, "errors": [f"missing schema: {SCHEMA_PATH.relative_to(ROOT)}"]}
    else:
        result = validate_registry(load_json(REGISTRY_PATH))

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS" if result.get("ok") else "FAIL")
        for error in result.get("errors", []):
            print(f"ERROR: {error}")
        for warning in result.get("warnings", []):
            print(f"WARNING: {warning}")

    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
