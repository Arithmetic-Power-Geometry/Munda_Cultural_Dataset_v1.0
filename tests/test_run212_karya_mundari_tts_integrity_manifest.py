import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/karya_mundari_tts_integrity_manifest_run212_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run212.jsonl"
COVERAGE = ROOT / "data/coverage_matrix.json"


def test_run212_karya_integrity_manifest_and_rights_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    rec = data["record"]
    recon = data["deterministic_reconciliation"]
    ver = data["verification"]
    gov = data["rights_access_consent_cultural_governance"]
    assert data["run"] == 212
    assert rec["repository"] == "karya-inc/dataset-mundari-tts"
    assert rec["repository_head_verified"] == "ea515f4d034a37e41e5b8619e1df62de0c7ee830"
    assert rec["readme_reported_total_recordings"] == 26870
    assert rec["readme_reported_female_recordings"] + rec["readme_reported_male_recordings"] == 26870
    assert rec["upstream_sha1_expected"] == "46c8bfceb5cf25decc8523479378793537f2bad7"
    assert rec["full_archive_filename_from_manifest"] == "dataset-mundari-tts-full.tgz"
    assert rec["license_name"] == "Karya Inc. Attribution-NonCommercial-ShareAlike-FreeSoftware 1.0 International Public License"
    assert recon["same_source_as_existing_karya_mundari_tts_lead"] is True
    assert recon["new_source_identity_created"] is False
    assert recon["26870_count_internal_arithmetic_consistency_verified"] is True
    assert recon["26868_vs_26870_cross_source_discrepancy_resolved"] is False
    assert ver["published_sha1_manifest_exact_value_verified"] is True
    assert ver["archive_bytes_verified"] is False
    assert ver["independent_sha1_verified"] is False
    assert ver["direct_audio_count_verified"] is False
    assert ver["linguistic_claim_promoted"] is False
    assert ver["cultural_claim_promoted"] is False
    assert gov["public_repository_is_not_participant_consent"] is True
    assert gov["community_validation_inferred"] is False
    assert gov["cultural_access_permission_inferred"] is False
    assert gov["participant_audio_or_transcript_ingested"] is False


def test_run212_counts_frozen_all_classes_and_coverage_contract_present():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000212"
    assert expected.issubset(set(row["classes"]))
    assert row["counts_changed"] is False
    assert row["audited_source_identities"] == 42
    assert row["unresolved_unique_web_leads"] == 73
    assert row["source_claims"] == 52
    assert row["evidence_records"] == 52
    assert row["evidence_links"] == 52
    assert row["streamlit_modules"] == 42
    assert row["cultural_claims_added"] == 0
    assert row["linguistic_claims_added"] == 0
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    assert coverage["sync_contract"] == "DATA TYPE↔SCHEMA↔SOURCE↔EVIDENCE↔STREAMLIT MODULE↔COVERAGE↔GAP"
    rows = {r["coverage_id"]: r for r in coverage["rows"]}
    assert rows["COV-008"]["gap_rule"] == "consent and rights required before public exposure"
    assert "never claim absolute completeness" in rows["COV-025"]["gap_rule"]
