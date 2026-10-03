import json
from pathlib import Path


def test_run242_orgi_c17_jharkhand_promotion_boundary():
    path = Path("data/source_census/orgi_c17_jharkhand_manifestation_run242_2026-09-12.json")
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["source"]["reference_id"] == "PC11_C17-20"
    assert data["source"]["declared_download_filename"] == "DDW-C17-2000.XLSX"
    schema = data["identity_and_schema_verification"]
    assert schema["munda_total_speakers_row_label_present_in_catalog_schema"] is True
    assert schema["mundari_total_speakers_row_label_present_in_catalog_schema"] is True

    integrity = data["byte_and_cell_integrity"]
    assert integrity["official_workbook_bytes_acquired"] is False
    assert integrity["independent_sha256_verified"] is False
    assert integrity["numeric_cells_promoted"] == 0

    boundary = data["evidence_promotion_boundary"]
    assert boundary["numeric_population_or_bilingualism_claims_promoted"] is False
    assert boundary["public_factual_claims_added"] == 0
    assert data["rights_and_governance"]["cultural_access_overrides_entitlement"] is True
