import json
from pathlib import Path


AUDIT = Path("data/source_census/ciet_ncert_barkhaa_mundari_manifestation_audit_run324_2026-09-14.json")


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run324_exact_mundari_title_locators_are_bounded():
    audit = load_audit()
    manifestations = audit["mundari_manifestations"]
    titles = manifestations["titles"]

    assert audit["run"] == 324
    assert audit["branch"] == "mlhkp-v2"
    assert audit["source"]["institution"] == "Central Institute of Educational Technology (CIET), NCERT"
    assert audit["source"]["first_party_locator"] == "https://ciet.ncert.gov.in/barkhaa_audio"
    assert manifestations["level"] == 1
    assert manifestations["exact_title_count"] == 9
    assert len(titles) == len(set(titles)) == 9
    assert "Tota" not in titles


def test_run324_does_not_overclaim_bytes_rights_or_cultural_permission():
    audit = load_audit()
    manifestations = audit["mundari_manifestations"]
    governance = audit["rights_and_governance"]
    promotion = audit["promotion"]

    assert manifestations["individual_audio_byte_urls_verified"] is False
    assert manifestations["individual_audio_bytes_acquired"] is False
    assert manifestations["individual_audio_hashes_verified"] is False
    assert governance["explicit_reuse_license_for_individual_mundari_audio_verified"] is False
    assert governance["speaker_or_performer_consent_verified"] is False
    assert governance["community_validation_verified"] is False
    assert governance["cultural_access_permission_verified"] is False
    assert promotion["new_controlled_cultural_claims"] == 0
    assert promotion["new_controlled_linguistic_claims"] == 0
    assert promotion["new_evidence_records"] == 0
    assert promotion["new_source_identity_count_increment"] == 0
