import json
from pathlib import Path


def test_run202_lexibank_peiros_exact_locator_boundary():
    p = Path("data/source_census/lexibank_peiros_v1_1_mundari_exact_locator_run202_2026-09-11.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    m = d["authoritative_or_primary_public_metadata"]
    v = d["verification_boundary"]
    r = d["rights_and_governance"]
    row = m["exact_locator"]["row_identity"]

    assert d["run"] == 202
    assert m["release_tag"] == "v1.1"
    assert m["version_doi"] == "10.5281/zenodo.13168443"
    assert m["dataset_license_statement"] == "CC-BY-4.0"
    assert m["exact_locator"]["file"] == "cldf/languages.csv"
    assert row["ID"] == row["Name"] == "Mundari"
    assert row["Glottocode"] == "mund1320"
    assert row["ISO639P3code"] == "unr"
    assert row["Family"] == "Austroasiatic"
    assert row["SubGroup"] == "MUNDA"

    assert v["v1_1_github_release_verified"] is True
    assert v["mundari_language_row_exactly_verified"] is True
    assert v["zenodo_release_archive_checksum_verified"] is False
    assert v["release_archive_bytes_independently_acquired"] is False
    assert v["mundari_lexical_rows_ingested"] == 0
    assert v["cultural_claims_added"] == 0
    assert v["evidence_graph_nodes_added"] == 0
    assert v["source_identities_added"] == 0

    assert r["underlying_peiros_source_rights_not_inferred_from_derived_dataset_license"] is True
    assert r["participant_consent_inferred"] is False
    assert r["community_validation_inferred"] is False
    assert r["cultural_access_permission_inferred"] is False
    assert r["cultural_access_overrides_legal_or_technical_entitlement"] is True
