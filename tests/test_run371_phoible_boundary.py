import json
from pathlib import Path


def test_phoible_lineage_does_not_promote_inventory_values_or_underlying_rights():
    p = Path("audits/phoible_mundari_inventory_lineage_run371_2026-09-15.json")
    d = json.loads(p.read_text(encoding="utf-8"))

    assert d["language_name"] == "Mundari"
    assert d["glottocode"] == "mund1320"
    assert d["iso639_3"] == "unr"
    assert len(d["provider_inventory_manifest"]) == 5

    ids = {x["inventory_id"] for x in d["provider_inventory_manifest"]}
    assert ids == {10, 602, 1713, 1770, 2295}

    vb = d["verification_boundary"]
    assert vb["provider_language_identity_verified"] is True
    assert vb["provider_declared_source_lineage_verified"] is True
    assert vb["underlying_source_passages_verified"] is False
    assert vb["inventory_rows_recomputed_from_download_bytes"] is False
    assert vb["download_bytes_sha256_verified"] is False
    assert vb["provider_license_treated_as_underlying_source_license"] is False
    assert vb["inventory_segment_values_promoted_to_controlled_evidence"] == 0
    assert vb["new_controlled_linguistic_claims_promoted"] == 0
    assert vb["new_controlled_cultural_claims_promoted"] == 0
    assert vb["community_validation_inferred"] is False
    assert vb["cultural_access_authorization_inferred"] is False

    c = d["canonicalization"]
    assert c["inventories_are_distinct_provider_manifestations"] is True
    assert c["bhumij_inventory_not_silently_collapsed_into_a_mundari_claim"] is True
