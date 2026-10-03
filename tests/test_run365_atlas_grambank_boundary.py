import json
from pathlib import Path


def _audit():
    path = Path("audits/original_atlas_grambank_exact_locator_run365_2026-09-15.json")
    return json.loads(path.read_text(encoding="utf-8"))


def test_run365_promotes_locators_not_claims():
    data = _audit()
    assert data["run"] == 365
    assert data["branch"] == "mlhkp-v2"
    assert data["controlled_count_change"] is False
    assert all(record["claim_promotion"] == 0 for record in data["records"])


def test_atlas_catalogue_not_misread_as_verified_pdf_or_distribution():
    data = _audit()
    atlases = [r for r in data["records"] if r["class"] == "maps_atlases_government"]
    assert {r["reference_id"] for r in atlases} == {
        "AA_2011_Jharkhand_vol1",
        "AA_2011_Jharkhand_vol2",
    }
    for record in atlases:
        assert record["promotion_level"] == "exact_provider_locator_only"
        assert "PDF bytes" in record["not_verified"]
        assert "Mundari-specific distribution" in record["not_verified"]
        assert "underlying demographic values" in record["not_verified"]


def test_grambank_license_does_not_expand_underlying_source_rights():
    data = _audit()
    grambank = next(r for r in data["records"] if r["provider"] == "Grambank")
    assert grambank["glottocode"] == "mund1320"
    assert grambank["provider_license"] == "Creative Commons Attribution 4.0 International License"
    assert "underlying-source reuse rights" in grambank["not_verified"]
    assert "independent source-to-feature trace-back" in grambank["not_verified"]
    assert "community validation" in grambank["not_verified"]
