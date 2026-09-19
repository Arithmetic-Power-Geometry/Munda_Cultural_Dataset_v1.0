#!/usr/bin/env python3
"""Deterministic page-accounting audit for MLHKP Encyclopaedia Mundarica artifacts.

This audit checks only repository page-block structure. It deliberately does NOT
certify scan comparison, transcription accuracy, cultural interpretation, or a
volume as VERIFIED COMPLETE.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data" / "source_bundles" / "encyclopaedia_mundarica"
AUDIT = BUNDLE / "completeness_audit.json"
PAGE_RE = re.compile(r"^##\s+(?:Scan|PDF)\s+page\s+(\d+)\s*$", re.I | re.M)


def analyse_page_blocks(path: Path, expected_pages: int) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = [int(x) for x in PAGE_RE.findall(text)]
    counts = {p: pages.count(p) for p in set(pages)}
    duplicates = sorted(p for p, n in counts.items() if n > 1)
    expected = set(range(1, expected_pages + 1))
    observed = set(pages)
    missing = sorted(expected - observed)
    out_of_range = sorted(observed - expected)
    ordered = pages == list(range(1, expected_pages + 1))
    return {
        "artifact": path.name,
        "declared_pages": expected_pages,
        "page_blocks_detected": len(pages),
        "first_page_block": pages[0] if pages else None,
        "last_page_block": pages[-1] if pages else None,
        "missing_page_blocks": missing,
        "duplicate_page_blocks": duplicates,
        "out_of_range_page_blocks": out_of_range,
        "strictly_ordered_contiguous_1_to_n": ordered,
        "page_accounting_complete": (
            len(pages) == expected_pages
            and not missing
            and not duplicates
            and not out_of_range
            and ordered
        ),
        "certifies_scan_comparison": False,
        "certifies_transcription_accuracy": False,
        "certifies_verified_complete": False,
    }


def volume1_result() -> dict:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    v1 = audit["volumes"][0]
    artifact = ROOT / v1["repository_artifact"]
    return analyse_page_blocks(artifact, int(v1["declared_scan_pages"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()
    result = volume1_result()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            "Mundarica V01 page accounting: "
            f"{result['page_blocks_detected']}/{result['declared_pages']} blocks; "
            f"continuous={result['page_accounting_complete']}"
        )
        if result["missing_page_blocks"]:
            print("Missing:", result["missing_page_blocks"])
        if result["duplicate_page_blocks"]:
            print("Duplicates:", result["duplicate_page_blocks"])
        if result["out_of_range_page_blocks"]:
            print("Out of range:", result["out_of_range_page_blocks"])
    return 0 if result["page_accounting_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
