import json
from pathlib import Path


def test_run201_mmloso_metadata_boundary():
    p = Path("data/source_census/mmloso_authoritative_metadata_run201_2026-09-11.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    a = d["authoritative_metadata"]
    v = d["verification_boundary"]
    r = d["rights_and_governance"]
    assert d["run"] == 201
    assert a["mundari_training_filename"] == "mundari-train.csv"
    assert a["mundari_training_columns"] == ["row_id", "hindi", "mundari"]
    assert a["declared_training_pairs_per_language_in_acl_findings"] == 20000
    assert a["declared_evaluation_sentences_in_acl_findings"] == 16000
    assert a["task_page_license_statement"] == "Creative Commons BY-SA 4.0"
    assert v["mundari_train_csv_independent_checksum_verified"] is False
    assert v["observed_file_row_count_independently_recomputed"] is False
    assert v["existing_16000_vs_15999_discrepancy_resolved"] is False
    assert v["dataset_rows_ingested"] == 0
    assert v["claims_added"] == v["evidence_records_added"] == v["evidence_links_added"] == 0
    assert r["participant_consent_inferred"] is False
    assert r["community_validation_inferred"] is False
    assert r["cultural_access_permission_inferred"] is False
    assert r["cultural_access_overrides_legal_or_technical_entitlement"] is True
