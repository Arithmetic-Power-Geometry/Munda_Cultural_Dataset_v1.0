import json
from pathlib import Path


def test_run204_mmloso_publication_count_reconciliation_boundary():
    p = Path("data/source_census/mmloso_16000_15999_publication_reconciliation_run204_2026-09-11.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    rec = d["deterministic_reconciliation"]
    gov = d["rights_and_governance"]
    prom = d["promotion"]

    assert d["run"] == 204
    assert d["source"]["anthology_id"] == "2025.mmloso-1.14"

    loc = {x["statement_type"]: x for x in d["exact_locators"]}
    assert loc["rounded/summary evaluation-set count"]["value"] == 16000
    assert loc["exact total test-sentence count in dataset description"]["value"] == 15999
    counts = loc["test-set language counts"]["values"]
    assert counts == {
        "Bhili": 1999,
        "English": 2000,
        "Gondi": 2000,
        "Hindi": 6000,
        "Mundari": 2000,
        "Santali": 2000,
    }
    assert sum(counts.values()) == 15999
    assert loc["training-set count"]["value"] == 20000

    assert rec["publication_internal_discrepancy_resolved"] is True
    assert rec["preferred_exact_publication_test_total"] == 15999
    assert rec["competition_file_independent_row_count_verified"] is False
    assert rec["competition_bytes_verified"] is False
    assert rec["independent_hash_verified"] is False
    assert rec["mundari_train_exact_file_rows_verified"] is False
    assert rec["test_csv_exact_file_rows_verified"] is False

    assert gov["dataset_license_reported_in_paper"] == "Creative Commons BY-SA 4.0"
    assert gov["license_extended_to_unverified_upstream_sources"] is False
    assert gov["participant_consent_inferred"] is False
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False
    assert gov["content_rows_ingested"] == 0

    assert prom["promote_exact_locator_count_reconciliation"] is True
    assert prom["promote_dataset_rows"] is False
    assert prom["promote_cultural_claims"] is False
    assert prom["create_new_source_identity"] is False
    assert prom["count_bearing_change"] is False
