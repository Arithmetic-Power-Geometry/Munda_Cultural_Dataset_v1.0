import json
from pathlib import Path


def test_muntts_karya_locator_does_not_promote_audio_without_governance():
    p = Path("audits/muntts_karya_exact_locator_rights_run373_2026-09-15.json")
    d = json.loads(p.read_text(encoding="utf-8"))

    assert d["canonical_work"]["anthology_id"] == "2024.computel-1.11"
    assert d["canonical_work"]["doi"] == "10.18653/v1/2024.computel-1.11"
    assert d["dataset_manifestation"]["repository_name"] == "dataset-mundari-tts"
    assert d["dataset_manifestation"]["provider_license_short"] == "KPL BY-NC-SA-FS 1.0"

    vb = d["verification_boundary"]
    assert vb["paper_bibliographic_identity_verified"] is True
    assert vb["dataset_repository_identity_verified"] is True
    assert vb["dataset_license_text_verified"] is True
    assert vb["sample_archive_bytes_materialized_and_sha256_verified"] is False
    assert vb["full_corpus_bytes_materialized_and_sha256_verified"] is False
    assert vb["recording_count_recomputed_from_archive"] is False
    assert vb["speaker_consent_documentation_verified"] is False
    assert vb["participant_privacy_publicity_clearance_verified"] is False
    assert vb["community_validation_verified"] is False
    assert vb["cultural_access_authorization_verified"] is False
    assert vb["audio_or_transcript_items_promoted_to_controlled_evidence"] == 0
    assert vb["paper_empirical_or_linguistic_claims_promoted_to_controlled_evidence"] == 0
    assert vb["new_controlled_cultural_claims_promoted"] == 0

    decision = d["ingestion_decision"]
    assert decision["paper_metadata_locator"] == "PROMOTE_EXACT_LOCATOR"
    assert decision["dataset_metadata_rights_locator"] == "PROMOTE_EXACT_LOCATOR"
    assert decision["sample_audio_transcripts"].startswith("HOLD_")
    assert decision["full_corpus"].startswith("HOLD_")
