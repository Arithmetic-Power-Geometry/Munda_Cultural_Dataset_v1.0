import json
from pathlib import Path


def test_run370_grambank_underlying_source_boundary():
    p = Path("audits/grambank_mundari_underlying_sources_run370_2026-09-15.json")
    data = json.loads(p.read_text(encoding="utf-8"))

    assert data["language_id"] == "mund1320"
    assert data["language_name"] == "Mundari"
    assert len(data["provider_declared_sources"]) == 3

    boundary = data["verification_boundary"]
    assert boundary["provider_language_identity_verified"] is True
    assert boundary["provider_declared_source_set_resolved_at_work_level"] is True
    assert boundary["raw_provenance_sheet_bytes_materialized"] is False
    assert boundary["raw_provenance_sheet_sha256_verified"] is False
    assert boundary["feature_rows_deterministically_recounted"] is False
    assert boundary["feature_to_source_mapping_verified"] is False
    assert boundary["source_passages_verified"] is False
    assert boundary["source_specific_reuse_permission_verified"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_authorization_inferred"] is False
    assert boundary["feature_values_promoted_to_controlled_evidence"] == 0
    assert boundary["linguistic_claims_promoted"] == 0
    assert boundary["cultural_claims_promoted"] == 0


def test_run370_grambank_sources_are_work_level_not_feature_evidence():
    data = json.loads(
        Path("audits/grambank_mundari_underlying_sources_run370_2026-09-15.json").read_text(
            encoding="utf-8"
        )
    )
    keys = {item["short_key"] for item in data["provider_declared_sources"]}
    assert keys == {"Cook 1965", "Osada 1992", "Osada 2008"}
    assert data["release_effect"].startswith("Grambank blocker narrowed")
