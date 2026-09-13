import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/ciil_sinha_1975_manifestation_audit_run314_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run314.jsonl"


def test_sinha_1975_manifestation_boundary():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["run"] == 314
    assert d["canonical_work"]["author"] == "N. K. Sinha"
    assert d["canonical_work"]["year"] == 1975
    assert d["repository_manifestation"]["handle"] == "20.500.14705/8179"
    assert d["repository_manifestation"]["file_name"] == "CIILP0091.pdf"
    assert d["repository_manifestation"]["repository_reported_file_size"] == "9.63 KB"
    q = d["quality_boundary"]
    assert q["full_book_bytes_independently_acquired"] is False
    assert q["independent_hash_computed"] is False
    assert q["page_inventory_verified"] is False
    assert q["repository_object_verified_as_complete_book"] is False
    assert q["ocr_verified"] is False
    assert q["linguistic_claims_promoted"] == 0
    assert q["cultural_claims_promoted"] == 0
    assert q["controlled_evidence_records_added"] == 0
    g = d["rights_governance_boundary"]
    assert not g["public_repository_access_treated_as_reuse_permission"]
    assert not g["copyright_notice_treated_as_participant_consent"]
    assert not g["community_validation_inferred"]
    assert not g["cultural_access_authorization_inferred"]


def test_run314_search_log_covers_all_controlled_classes():
    rows = [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 14
    assert len({r["class"] for r in rows}) == 14
    assert all(r["run"] == 314 for r in rows)
