import json
from pathlib import Path


def test_run364_asjp_source_boundary():
    path = Path("data/source_census/asjp_mundari_wordlist_source_audit_run364_2026-09-15.json")
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["branch"] == "mlhkp-v2"
    assert data["language_identity"]["iso_639_3"] == "unr"
    assert data["language_identity"]["glottocode"] == "mund1320"
    assert len(data["observed_provider_records"]) == 2

    verification = data["verification"]
    assert verification["two_distinct_asjp_mundari_wordlist_records_verified"] is True
    assert verification["declared_source_genealogy_verified_on_provider_pages"] is True
    assert verification["source_work_pages_or_entries_independently_verified"] is False
    assert verification["asjp_export_bytes_materialized"] is False
    assert verification["asjp_export_sha256_verified"] is False
    assert verification["asjp_export_row_count_verified"] is False
    assert verification["lexical_items_promoted_to_controlled_evidence"] is False
    assert verification["cultural_claims_promoted"] is False

    canonicalization = data["canonicalization"]
    assert canonicalization["treat_MUNDARI_and_MUNDARI_2_as_two_provider_wordlist_manifestations"] is True
    assert canonicalization["do_not_treat_them_as_two_distinct_language_identities"] is True
    assert canonicalization["controlled_identity_count_changed"] is False

    governance = data["rights_governance"]
    assert governance["database_license_is_underlying_source_reuse_permission"] is False
    assert governance["database_public_visibility_is_community_validation"] is False
    assert governance["lexical_database_record_is_cultural_authorization"] is False
    assert governance["cultural_access_overrides_entitlement"] is True
