import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/muntts_paper_karya_dataset_relationship_run156_2026-09-10.json"


def test_muntts_paper_dataset_relationship_is_distinct_and_rights_safe():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["web_source_id"] == "WEB-MUN-0090"
    assert data["paper"]["doi"] == "10.18653/v1/2024.computel-1.11"
    assert data["relationship"]["decision"] == "related_distinct_source_objects"
    assert data["relationship"]["dedupe_decision"] == "do_not_collapse_paper_identity_into_dataset_repository_identity"
    assert data["permitted_promotion_boundary"]["audio_bytes"] is False
    assert data["permitted_promotion_boundary"]["transcript_text"] is False
    assert data["permitted_promotion_boundary"]["consent_inference"] is False
    assert data["rights_governance"]["cultural_access_overrides_entitlement"] is True
    assert data["master_reconciliation"]["permanent_src_mmsc_assignment_this_run"] is False


def test_muntts_count_discrepancy_is_preserved_not_fabricated_away():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["dataset"]["upstream_reported_recordings"] == 26870
    assert "26,868" in data["relationship"]["numeric_difference_not_normalized_away"]
    assert "not verified" in data["relationship"]["numeric_difference_not_normalized_away"]
