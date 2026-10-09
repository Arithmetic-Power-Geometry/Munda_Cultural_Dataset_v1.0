import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run177_registration_blocker_is_closed_as_existing_identity():
    audit = load_json("data/source_census/kumari_rahman_run177_stale_blocker_resolution_run178_2026-09-11.json")
    prior = load_json("data/source_census/kumari_rahman_2021_existing_identity_reconciliation_run172_2026-09-10.json")
    discoveries = load_json("data/source_census/mmsc_discoveries.json")
    index = load_json("data/source_census/mmsc_index.json")

    records = {r["source_id"]: r for r in discoveries["records"]}
    source = records["SRC-MMSC-000003"]
    assert source["identifier"]["scheme"] == "DOI"
    assert source["identifier"]["value"].lower() == "10.35784/pe.2021.1.19"
    assert prior["deterministic_reconciliation"]["decision"] == "already_registered_permanent_identity"
    assert audit["repository_reconciliation"]["existing_source_id"] == "SRC-MMSC-000003"
    assert audit["repository_reconciliation"]["run177_pending_registration_blocker"] == "stale_and_closed"
    assert audit["repository_reconciliation"]["new_identity_created"] is False
    assert audit["repository_reconciliation"]["counts_changed"] is False
    assert index["metrics"]["sources_discovered"] == 42


def test_run178_preserves_evidence_and_cultural_access_boundaries():
    audit = load_json("data/source_census/kumari_rahman_run177_stale_blocker_resolution_run178_2026-09-11.json")
    evidence = audit["evidence_boundary"]
    rights = audit["rights_governance"]
    assert evidence["new_claim_added"] is False
    assert evidence["new_evidence_record_added"] is False
    assert evidence["new_evidence_link_added"] is False
    assert evidence["participant_material_ingested"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_permission_inferred"] is False
    assert rights["cultural_access_overrides_entitlement"] is True
