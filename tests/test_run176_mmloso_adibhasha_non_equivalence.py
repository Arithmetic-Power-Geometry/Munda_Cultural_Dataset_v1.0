import json
from pathlib import Path


def test_run176_mmloso_adibhasha_non_equivalence_boundary():
    p = Path("data/source_census/mmloso_adibhasha_non_equivalence_run176_2026-09-11.json")
    audit = json.loads(p.read_text(encoding="utf-8"))
    assert audit["run"] == 176
    assert audit["shared_task_paper"]["acl_anthology_id"] == "2025.mmloso-1.14"
    assert audit["current_related_dataset_card"]["repository"] == "misniitdelhi/AdiBhasha"
    assert audit["deterministic_reconciliation"]["same_manifestation_verified"] is False
    assert audit["deterministic_reconciliation"]["same_version_verified"] is False
    assert audit["deterministic_reconciliation"]["same_row_set_verified"] is False
    assert audit["promotion_decision"]["dataset_rows_ingested"] == 0
    assert audit["promotion_decision"]["paper_to_dataset_identity_collapse"] is False
    assert audit["rights_governance"]["gated_access_overridden"] is False
    assert audit["rights_governance"]["community_validation_inferred"] is False
    assert audit["rights_governance"]["cultural_access_permission_inferred"] is False
    assert audit["release_effect"]["audited_source_identity_count_change"] == 0


def test_run176_preserves_cultural_access_precedence():
    audit = json.loads(Path("data/source_census/mmloso_adibhasha_non_equivalence_run176_2026-09-11.json").read_text(encoding="utf-8"))
    assert audit["rights_governance"]["cultural_access_overrides_entitlement"] is True
    assert audit["rights_governance"]["public_card_visibility_is_permission"] is False
