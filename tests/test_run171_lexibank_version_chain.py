import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run171_version_chain_is_verified_but_not_count_bearing():
    audit = load("data/source_census/lexibank_peiros_version_chain_verification_run171_2026-09-10.json")
    chain = audit["version_chain_evidence"]
    recon = audit["deterministic_reconciliation"]
    assert chain["v1_0"]["zenodo_doi"] == "10.5281/zenodo.5127536"
    assert chain["v1_1"]["zenodo_doi"] == "10.5281/zenodo.13168443"
    assert chain["v1_0"]["registry_reports_versions"] == ["v1.1", "v1.0"]
    assert chain["v1_1"]["registry_reports_versions"] == ["v1.1", "v1.0"]
    assert chain["relationship_state"] == "same_dataset_version_series_independently_corroborated"
    assert recon["version_relationship_verified"] is True
    assert recon["direct_current_zenodo_manifestation_verified"] is False
    assert audit["promotion"]["new_permanent_identity_created"] is False
    assert audit["promotion"]["counts_changed"] is False
    assert audit["promotion"]["dataset_rows_ingested"] is False
    assert audit["promotion"]["lexical_forms_ingested"] is False
    assert audit["promotion"]["cognate_assignments_ingested"] is False
    assert audit["rights_and_cultural_access"]["participant_consent_inferred"] is False
    assert audit["rights_and_cultural_access"]["community_validation_inferred"] is False
    assert audit["rights_and_cultural_access"]["cultural_access_permission_inferred"] is False


def test_run171_full_class_sweep_and_release_counts_are_synchronized():
    log = json.loads((ROOT / "data/source_census/search_log_run171.jsonl").read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers", "web_resources", "datasets", "audio", "video",
        "maps", "relevant_media",
    }
    assert set(log["classes_requested"]) == expected
    mmsc = load("data/source_census/mmsc_index.json")["metrics"]
    release = load("publication/generated/release_metrics.json")
    assert mmsc["sources_discovered"] == release["sources_discovered"] == 42
    assert mmsc["web_discovery_records_observed"] == release["web_discovery_records_observed"] == 90
    assert mmsc["web_discovery_unique_leads"] == release["web_discovery_unique_leads"] == 87
    assert mmsc["web_discovery_duplicate_records"] == release["web_discovery_duplicate_records"] == 3
    assert mmsc["web_discovery_leads_counted_in_audited_identity_total"] == release["web_discovery_leads_counted_in_audited_identity_total"] == 14
    assert mmsc["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == release["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 73
    assert release["source_claims"] == 52
    assert release["evidence_records"] == 52
    assert release["evidence_links"] == 52
    assert release["registered_streamlit_modules"] == 42
