import json
from pathlib import Path


def test_phoible_raw_mapping_boundary_preserves_1713_conflict():
    audit = json.loads(
        Path("audits/phoible_raw_mapping_crosscheck_run372_2026-09-15.json").read_text(encoding="utf-8")
    )
    rows = {row["inventory_id"]: row for row in audit["inventory_crosscheck"]}
    assert set(rows) == {10, 602, 1713, 1770, 2295}
    assert rows[1713]["upstream_language_label"] == "Bhumij"
    assert rows[1713]["glottocode"] == "mund1320"
    assert "not silently promotable" in rows[1713]["classification"]

    boundary = audit["verification_boundary"]
    assert boundary["upstream_mapping_rows_observed_at_pinned_commit"] is True
    assert boundary["inventory_1713_label_conflict_preserved"] is True
    assert boundary["inventory_1713_promoted_as_mundari_phonological_evidence"] is False
    assert boundary["raw_inventory_segment_rows_materialized_and_recounted"] is False
    assert boundary["underlying_source_passages_verified"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_authorization_inferred"] is False
    assert boundary["new_controlled_linguistic_claims_promoted"] == 0
    assert boundary["new_controlled_cultural_claims_promoted"] == 0
