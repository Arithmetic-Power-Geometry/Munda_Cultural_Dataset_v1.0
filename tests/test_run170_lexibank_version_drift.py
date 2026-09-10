import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run170_lexibank_version_drift_is_not_count_bearing():
    audit = load("data/source_census/lexibank_peiros_version_drift_run170_2026-09-10.json")
    assert audit["prior_repository_observation"]["recorded_version"] == "v1.0"
    assert audit["prior_repository_observation"]["recorded_zenodo_doi"] == "10.5281/zenodo.5127536"
    assert audit["current_live_manifestation"]["observed_version"] == "v1.1"
    assert audit["current_live_manifestation"]["observed_zenodo_doi"] == "10.5281/zenodo.13168443"
    assert audit["deterministic_reconciliation"]["candidate_identity_collision_resolved"] is False
    assert audit["promotion"]["new_permanent_identity_created"] is False
    assert audit["promotion"]["counts_changed"] is False
    assert audit["promotion"]["dataset_rows_ingested"] is False
    assert audit["promotion"]["lexical_forms_ingested"] is False
    assert audit["promotion"]["cognate_assignments_ingested"] is False
    assert audit["rights_and_cultural_access"]["participant_consent_inferred"] is False
    assert audit["rights_and_cultural_access"]["community_validation_inferred"] is False
    assert audit["rights_and_cultural_access"]["cultural_access_permission_inferred"] is False


def test_run170_does_not_change_release_counts():
    mmsc = load("data/source_census/mmsc_index.json")
    mm = mmsc["metrics"]
    assert mm["sources_discovered"] == 42
    assert mm["web_discovery_records_observed"] == 90
    assert mm["web_discovery_unique_leads"] == 87
    assert mm["web_discovery_duplicate_records"] == 3
    assert mm["web_discovery_leads_counted_in_audited_identity_total"] == 14
    assert mm["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 73
