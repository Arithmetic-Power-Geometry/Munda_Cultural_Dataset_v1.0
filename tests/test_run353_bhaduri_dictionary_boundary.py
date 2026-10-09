import json
from pathlib import Path


AUDIT = Path("data/source_census/bhaduri_mundari_english_dictionary_exact_locator_run353_2026-09-14.json")


def test_run353_bhaduri_exact_locator_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["run"] == 353
    assert data["deterministic_identity_key"] == "Bhaduri|A Mundari-English dictionary|1931-original-work"
    assert data["permitted_promotion"]["source_identity"] is True
    assert data["permitted_promotion"]["stable_catalogue_identifiers"] is True
    assert data["permitted_promotion"]["dictionary_entries"] is False
    assert data["permitted_promotion"]["lexical_claims"] is False
    assert data["permitted_promotion"]["page_exact_lexical_evidence"] is False
    assert data["permitted_promotion"]["full_text_bytes_verified"] is False
    assert data["permitted_promotion"]["independent_sha256_verified"] is False
    assert data["permitted_promotion"]["reuse_license_verified"] is False
    assert data["permitted_promotion"]["community_validation_verified"] is False
    assert data["permitted_promotion"]["cultural_access_authorization_verified"] is False


def test_run353_reprints_are_not_counted_as_independent_sources():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    rule = data["canonicalization_rule"].lower()
    assert "one underlying 1931 work identity" in rule
    assert "must not be counted as independent" in rule
