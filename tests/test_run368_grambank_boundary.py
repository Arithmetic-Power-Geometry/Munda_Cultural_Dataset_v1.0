import json
from pathlib import Path


def test_run368_grambank_mundari_provenance_boundary():
    path = Path("audits/grambank_mundari_provenance_run368_2026-09-15.json")
    data = json.loads(path.read_text(encoding="utf-8"))

    lang = data["language_table"]
    boundary = data["verification_boundary"]

    assert lang["language_id"] == "mund1320"
    assert lang["name"] == "Mundari"
    assert lang["glottocode"] == "mund1320"
    assert lang["provenance_sheet"] == "TWI_mund1320.tsv"
    assert boundary["provider_language_identity_verified"] is True
    assert boundary["exact_provider_provenance_sheet_name_verified"] is True

    # Provider visibility/licensing must never be promoted into unverified
    # feature evidence, linguistic/cultural claims, community validation, or
    # cultural-access authorization.
    assert boundary["provenance_sheet_bytes_materialized"] is False
    assert boundary["underlying_source_passages_verified"] is False
    assert boundary["feature_values_promoted_to_controlled_evidence"] == 0
    assert boundary["linguistic_claims_promoted"] == 0
    assert boundary["cultural_claims_promoted"] == 0
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_authorization_inferred"] is False
