import json
from pathlib import Path


def test_run203_peiros_zenodo_manifestation_boundary():
    p = Path("data/source_census/lexibank_peiros_v1_1_zenodo_manifest_run203_2026-09-11.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    r = d["record"]
    v = d["verification_boundary"]
    g = d["rights_and_governance"]

    assert d["run"] == 203
    assert r["version"] == "v1.1"
    assert r["version_doi"] == "10.5281/zenodo.13168443"
    assert r["archive_filename"] == "lexibank/peirosaustroasiatic-v1.1.zip"
    assert r["repository_reported_checksum_algorithm"] == "md5"
    assert r["repository_reported_checksum"] == "cff41a8a9db0f74e14550d2330a56483"

    assert v["zenodo_landing_record_retrieved"] is True
    assert v["archive_filename_verified_from_zenodo"] is True
    assert v["repository_reported_md5_verified_as_metadata"] is True
    assert v["archive_bytes_independently_acquired"] is False
    assert v["independent_md5_recomputed"] is False
    assert v["forms_csv_bytes_independently_verified"] is False
    assert v["mundari_lexical_rows_ingested"] == 0
    assert v["source_identities_added"] == 0
    assert v["claims_added"] == 0
    assert v["evidence_records_added"] == 0
    assert v["evidence_links_added"] == 0

    assert g["underlying_peiros_source_rights_inferred"] is False
    assert g["participant_consent_inferred"] is False
    assert g["community_validation_inferred"] is False
    assert g["cultural_access_permission_inferred"] is False
    assert g["cultural_access_overrides_legal_or_technical_entitlement"] is True
