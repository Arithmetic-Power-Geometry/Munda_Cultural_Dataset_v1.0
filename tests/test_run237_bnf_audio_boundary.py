import json
from pathlib import Path


AUDIT = Path("data/source_census/bnf_historical_mundari_audio_locator_audit_run237_2026-09-12.json")


def test_run237_archive_locator_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    records = data["records"]
    assert [r["web_source_id"] for r in records] == ["WEB-MUN-0018", "WEB-MUN-0019", "WEB-MUN-0020"]
    assert len({r["ark"] for r in records}) == 3
    assert all(r["verification_state"].startswith("national_library_catalogue_exact_locator_verified") for r in records)

    governance = data["rights_and_governance"]
    assert governance["public_catalogue_visibility_is_permission"] is False
    assert governance["digital_holding_presence_is_redistribution_permission"] is False
    assert governance["historical_recording_is_community_validation"] is False
    assert governance["participant_or_performer_consent_inferred"] is False
    assert governance["cultural_access_permission_inferred"] is False
    assert governance["audio_bytes_acquired"] is False
    assert governance["transcripts_or_translations_ingested"] is False
    assert governance["public_factual_cultural_claims_added"] == 0

    durang = next(r for r in records if r["web_source_id"] == "WEB-MUN-0020")
    assert durang["independent_catalogue_corroboration"]["shelfmark"] == "IOR/S/2/1/17"
    assert "identity/provenance only" in durang["promotion_boundary"]
