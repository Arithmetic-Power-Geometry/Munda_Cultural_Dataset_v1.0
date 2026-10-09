"""Recompute conservative identity upper bounds from immutable WEB-MUN records.

Only independently audited exact-work equivalences are merged. Unreviewed
similar titles and shared source families are NOT automatically merged.
Output is an upper bound, never a certified exact count or cultural evidence.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "data" / "source_census"


def audited_bounds():
    documents = [json.loads(p.read_text(encoding="utf-8"))
                 for p in sorted(CENSUS.glob("web_discovery*.json"))]
    records = [r for doc in documents for r in doc.get("records", [])]
    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate immutable WEB-MUN observation ID")
    parent = {identifier: identifier for identifier in ids}

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def merge(a, b):
        if a not in parent or b not in parent:
            raise ValueError(f"Missing WEB-MUN identity in verified pair: {a}, {b}")
        a, b = root(a), root(b)
        if a != b:
            parent[max(a, b)] = min(a, b)

    a822 = json.loads((CENSUS / "run822_web_duplicate_pairs_audit_2026-10-09.json").read_text(encoding="utf-8"))
    a824 = json.loads((CENSUS / "run824_three_additional_duplicate_reconciliations_2026-10-09.json").read_text(encoding="utf-8"))
    web_pairs = []
    external_matches = []
    for a, b, reason in a822["additional_exact_identity_duplicate_pairs"] + a822["already_indexed_duplicate_pairs"]:
        if a.startswith("WEB-MUN-") and b.startswith("WEB-MUN-"):
            merge(a, b)
            web_pairs.append((a, b, reason))
        else:
            external_matches.append((a, b, reason))
    for pair in a824["duplicate_relationships"]:
        merge(pair["canonical"], pair["duplicate"])
        web_pairs.append((pair["canonical"], pair["duplicate"], pair["key"]))
    components = {}
    for identifier in ids:
        components.setdefault(root(identifier), []).append(identifier)
    external_components = set()
    for a, b, reason in external_matches:
        web_id = a if a.startswith("WEB-MUN-") else b
        external_id = b if web_id == a else a
        if web_id not in parent or not external_id.startswith("SRC-MMSC-"):
            raise ValueError(f"Unexpected external identity: {a}, {b}")
        external_components.add(root(web_id))
    return {
        "raw_observations": len(ids),
        "source_manifest_count": len(documents),
        "audited_web_equivalence_pairs": len(web_pairs),
        "web_identity_component_upper_bound": len(components),
        "web_components_matched_to_known_standalone": len(external_components),
        "additional_web_work_upper_bound_after_known_standalone_matches": len(components) - len(external_components),
        "certified_exact_unique_work_count": None,
        "uncertainty": "Additional collisions and catalogue-section/edition relationships remain unreviewed.",
        "rights_and_cultural_claims_promoted": 0,
    }


if __name__ == "__main__":
    print(json.dumps(audited_bounds(), indent=2))
