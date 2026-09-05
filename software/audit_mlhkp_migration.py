#!/usr/bin/env python3
"""MLHKP v2 migration/integrity audit.

Checks the inherited MCD seed data before large-scale enrichment.
Uses only Python standard library so it can run locally and in GitHub Actions.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

EXPECTED = {
    "cultural_domains.csv": 24,
    "cultural_subdomains.csv": 266,
    "cultural_indicators.csv": 798,
    "sources.csv": 14,
    "source_claims.csv": 38,
    "evidence.csv": 38,
    "evidence_links.csv": 38,
}

ID_COLUMNS = {
    "cultural_domains.csv": "domain_id",
    "cultural_subdomains.csv": "subdomain_id",
    "cultural_indicators.csv": "indicator_id",
    "sources.csv": "source_id",
    "source_claims.csv": "claim_id",
    "evidence.csv": "evidence_id",
    "evidence_links.csv": "link_id",
}


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA / name
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def duplicate_values(rows: list[dict[str, str]], col: str) -> list[str]:
    values = [r.get(col, "").strip() for r in rows if r.get(col, "").strip()]
    return sorted(v for v, n in Counter(values).items() if n > 1)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    tables: dict[str, list[dict[str, str]]] = {}

    for name, expected in EXPECTED.items():
        try:
            rows = read_csv(name)
            tables[name] = rows
        except FileNotFoundError:
            errors.append(f"Missing required file: data/{name}")
            continue
        if len(rows) != expected:
            errors.append(f"data/{name}: expected {expected} rows, found {len(rows)}")
        id_col = ID_COLUMNS[name]
        dups = duplicate_values(rows, id_col)
        if dups:
            errors.append(f"data/{name}: duplicate {id_col}: {', '.join(dups[:10])}")

    if errors:
        report = {"status": "FAIL", "errors": errors, "warnings": warnings}
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1

    domains = {r["domain_id"] for r in tables["cultural_domains.csv"]}
    subdomains = {r["subdomain_id"] for r in tables["cultural_subdomains.csv"]}
    indicators = {r["indicator_id"] for r in tables["cultural_indicators.csv"]}
    sources = {r["source_id"] for r in tables["sources.csv"]}
    claims = {r["claim_id"] for r in tables["source_claims.csv"]}
    evidence = {r["evidence_id"] for r in tables["evidence.csv"]}

    # Referential integrity: subdomains -> domains.
    for r in tables["cultural_subdomains.csv"]:
        if r.get("domain_id") not in domains:
            errors.append(f"Orphan subdomain {r.get('subdomain_id')}: domain {r.get('domain_id')} missing")

    # Indicators -> domains/subdomains.
    for r in tables["cultural_indicators.csv"]:
        if r.get("domain_id") not in domains:
            errors.append(f"Indicator {r.get('indicator_id')}: domain {r.get('domain_id')} missing")
        if r.get("subdomain_id") not in subdomains:
            errors.append(f"Indicator {r.get('indicator_id')}: subdomain {r.get('subdomain_id')} missing")

    # Claims -> source/domain/subdomain.
    for r in tables["source_claims.csv"]:
        if r.get("source_id") not in sources:
            errors.append(f"Claim {r.get('claim_id')}: source {r.get('source_id')} missing")
        if r.get("domain_id") not in domains:
            errors.append(f"Claim {r.get('claim_id')}: domain {r.get('domain_id')} missing")
        if r.get("subdomain_id") not in subdomains:
            errors.append(f"Claim {r.get('claim_id')}: subdomain {r.get('subdomain_id')} missing")

    # Evidence -> source/claim.
    for r in tables["evidence.csv"]:
        if r.get("source_id") and r.get("source_id") not in sources:
            errors.append(f"Evidence {r.get('evidence_id')}: source {r.get('source_id')} missing")
        if r.get("claim_id") and r.get("claim_id") not in claims:
            errors.append(f"Evidence {r.get('evidence_id')}: claim {r.get('claim_id')} missing")
        if not r.get("access_level", "").strip():
            warnings.append(f"Evidence {r.get('evidence_id')}: access_level blank")

    # Evidence links -> claims/evidence for current seed link types.
    for r in tables["evidence_links.csv"]:
        ftype, fid = r.get("from_type", ""), r.get("from_id", "")
        ttype, tid = r.get("to_type", ""), r.get("to_id", "")
        if ftype == "claim" and fid not in claims:
            errors.append(f"Link {r.get('link_id')}: claim {fid} missing")
        if ttype == "claim" and tid not in claims:
            errors.append(f"Link {r.get('link_id')}: claim {tid} missing")
        if ftype == "evidence" and fid not in evidence:
            errors.append(f"Link {r.get('link_id')}: evidence {fid} missing")
        if ttype == "evidence" and tid not in evidence:
            errors.append(f"Link {r.get('link_id')}: evidence {tid} missing")

    # Every seed claim should currently have direct evidence and at least one evidence link.
    evidenced_claims = {r.get("claim_id") for r in tables["evidence.csv"] if r.get("claim_id")}
    linked_claims = set()
    for r in tables["evidence_links.csv"]:
        if r.get("from_type") == "claim":
            linked_claims.add(r.get("from_id"))
        if r.get("to_type") == "claim":
            linked_claims.add(r.get("to_id"))
    missing_evidence = sorted(claims - evidenced_claims)
    missing_links = sorted(claims - linked_claims)
    if missing_evidence:
        errors.append(f"Claims without evidence rows: {', '.join(missing_evidence)}")
    if missing_links:
        errors.append(f"Claims without evidence links: {', '.join(missing_links)}")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "counts": {name: len(rows) for name, rows in tables.items()},
        "integrity": {
            "duplicate_core_ids": 0 if not errors else "see errors",
            "orphan_subdomains": 0 if not any("Orphan subdomain" in e for e in errors) else "see errors",
            "claims_without_evidence": len(missing_evidence),
            "claims_without_evidence_links": len(missing_links),
        },
        "warnings": warnings,
        "errors": errors,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
