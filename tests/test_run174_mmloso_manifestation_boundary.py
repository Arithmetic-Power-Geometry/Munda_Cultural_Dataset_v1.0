import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/mmloso_manifestation_reconciliation_run174_2026-09-10.json"
MMSC = ROOT / "data/source_census/mmsc_index.json"


def test_mmloso_manifestation_boundary_is_conservative():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["paper"]["identity_verified"] is True
    assert audit["paper_reported_dataset_facts"]["count_discrepancy_preserved"] is True
    assert audit["related_manifestation"]["same_manifestation_as_paper_release_verified"] is False
    assert audit["related_manifestation"]["row_level_license_equivalence_verified"] is False
    assert audit["governance_boundary"]["parallel_rows_ingested"] is False
    assert audit["governance_boundary"]["community_validation_claimed"] is False
    assert audit["governance_boundary"]["copyright_or_technical_entitlement_does_not_override_cultural_access"] is True
    assert audit["count_effect"] == {
        "audited_source_identities_delta": 0,
        "claims_delta": 0,
        "evidence_records_delta": 0,
        "evidence_links_delta": 0,
    }


def test_run174_does_not_inflate_census_counts():
    mmsc = json.loads(MMSC.read_text(encoding="utf-8"))
    assert mmsc["metrics"]["sources_discovered"] == 42
    assert mmsc["metrics"]["standalone_mmsc_discoveries"] == 16
    assert mmsc["metrics"]["web_discovery_records_observed"] == 90
    assert mmsc["metrics"]["web_discovery_unique_leads"] == 87
    assert mmsc["metrics"]["web_discovery_duplicate_records"] == 3
    assert mmsc["metrics"]["web_discovery_leads_counted_in_audited_identity_total"] == 14
    assert mmsc["metrics"]["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 73
