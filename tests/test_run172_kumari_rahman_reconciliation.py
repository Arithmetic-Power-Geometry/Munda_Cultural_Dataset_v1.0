import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_kumari_rahman_is_existing_identity_not_new_source():
    audit = load_json("data/source_census/kumari_rahman_2021_existing_identity_reconciliation_run172_2026-09-10.json")
    discoveries = load_json("data/source_census/mmsc_discoveries.json")
    index = load_json("data/source_census/mmsc_index.json")

    records = {r["source_id"]: r for r in discoveries["records"]}
    source = records["SRC-MMSC-000003"]

    assert source["identifier"]["scheme"] == "DOI"
    assert source["identifier"]["value"].lower() == "10.35784/pe.2021.1.19"
    assert audit["deterministic_reconciliation"]["existing_source_id"] == "SRC-MMSC-000003"
    assert audit["deterministic_reconciliation"]["new_identity_created"] is False
    assert audit["deterministic_reconciliation"]["mmsc_counts_changed"] is False
    assert index["metrics"]["sources_discovered"] == 42
    assert index["metrics"]["standalone_mmsc_discoveries"] == 16


def test_run172_does_not_expand_rights_or_evidence():
    audit = load_json("data/source_census/kumari_rahman_2021_existing_identity_reconciliation_run172_2026-09-10.json")
    boundary = audit["evidence_boundary"]
    governance = audit["rights_governance"]

    assert boundary["new_claim_added"] is False
    assert boundary["new_evidence_record_added"] is False
    assert boundary["new_evidence_link_added"] is False
    assert boundary["participant_material_ingested"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_permission_inferred"] is False
    assert governance["public_availability_is_not_permission"] is True
    assert governance["cultural_access_overrides_entitlement"] is True
