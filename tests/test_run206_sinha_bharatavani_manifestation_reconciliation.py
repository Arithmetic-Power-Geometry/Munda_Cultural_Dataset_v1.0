import json
from pathlib import Path


def test_run206_sinha_bharatavani_manifestation_boundary():
    p = Path("data/source_census/sinha_1975_ciil_bharatavani_manifestation_reconciliation_run206_2026-09-11.json")
    d = json.loads(p.read_text(encoding="utf-8"))

    assert d["run"] == 206
    assert d["work"]["title"] == "Mundari Grammar"
    assert d["work"]["author"] == "N. K. Sinha"
    assert d["work"]["year"] == 1975
    assert d["work"]["new_permanent_source_identity_created"] is False

    by_system = {m["system"]: m for m in d["official_manifestations"]}
    sanchika = by_system["Bhasha Sanchika — CIIL Repository"]
    bharatavani = by_system["Bharatavani"]
    assert sanchika["handle"] == "20.500.14705/8179"
    assert sanchika["repository_identifier"] == "CIILP0091"
    assert sanchika["reported_file_size"] == "9.63 KB"
    assert sanchika["full_text_verified"] is False
    assert bharatavani["reported_file_size"] == "117.39 MB"
    assert bharatavani["access_statement"] == "Login to Read"
    assert bharatavani["bytes_acquired"] is False
    assert bharatavani["full_text_verified"] is False

    r = d["reconciliation"]
    assert r["same_bibliographic_work_supported"] is True
    assert r["same_digital_file_claimed"] is False
    assert r["sanchika_cover_is_not_full_book"] is True
    assert r["bharatavani_117_39mb_is_not_treated_as_acquired"] is True
    assert r["login_gate_preserved"] is True

    b = d["rights_access_cultural_boundary"]
    assert b["public_catalogue_visibility_is_permission"] is False
    assert b["login_access_is_redistribution_permission"] is False
    assert b["model_training_permission_verified"] is False
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False
    assert b["grammar_rules_promoted"] == 0
    assert b["lexical_rows_promoted"] == 0
    assert b["cultural_claims_promoted"] == 0

    e = d["release_effect"]
    assert e["discovery_only_state_reduced"] is True
    assert e["exact_official_catalogue_locator_added"] is True
    assert e["full_text_ingestion_completed"] is False
    assert e["source_identities_added"] == 0
    assert e["claims_added"] == 0
    assert e["evidence_records_added"] == 0
    assert e["evidence_links_added"] == 0
    assert e["streamlit_modules_added"] == 0
    assert e["count_bearing_change"] is False
