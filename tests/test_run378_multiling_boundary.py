import json
from pathlib import Path


def test_multiling_munda_remains_discovery_only_without_item_governance():
    p = Path("data/source_census/bangladesh_multiling_munda_exact_locator_run378_2026-09-15.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["verification_state"]["identity"] == "verified_provider_surface"
    assert d["verification_state"]["item_level_reuse_rights"] == "not_verified"
    assert d["verification_state"]["speaker_identity_and_consent"] == "not_verified"
    assert d["verification_state"]["cultural_access_authorization"] == "not_verified"
    assert d["promotion"]["public_factual_claim_promoted"] is False
    assert d["promotion"]["audio_or_transcript_ingested"] is False


def test_provider_archive_counts_are_not_treated_as_deterministic_recount():
    p = Path("data/source_census/bangladesh_multiling_munda_exact_locator_run378_2026-09-15.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["verification_state"]["archive_count"] == "provider_reported_not_deterministically_recounted"
    assert d["verification_state"]["audio_minutes"] == "provider_reported_not_deterministically_recounted"
    assert d["verification_state"]["cryptographic_hash"] == "not_verified"
    assert d["deduplication"]["do_not_expand_each_archive_unit_as_identity"] is True
