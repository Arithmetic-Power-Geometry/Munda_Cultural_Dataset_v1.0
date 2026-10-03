import json
from pathlib import Path


def test_run363_st16_locator_boundary():
    path = Path("data/source_census/census_st16_jharkhand_exact_locator_run363_2026-09-15.json")
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["branch"] == "mlhkp-v2"
    assert data["canonical_work"]["reference_id"] == "PC11_ST16-20"
    assert data["canonical_work"]["declared_manifestation"] == "ST-20-00-16-DDW-2011.XLSX"

    verification = data["verification"]
    assert verification["provider_identity_verified"] is True
    assert verification["reference_id_verified"] is True
    assert verification["declared_workbook_filename_verified"] is True
    assert verification["workbook_bytes_obtained"] is False
    assert verification["sha256_verified"] is False
    assert verification["sheet_inventory_verified"] is False
    assert verification["row_locators_verified"] is False
    assert verification["cell_locators_verified"] is False
    assert verification["numeric_values_promoted"] is False
    assert verification["mundari_specific_row_content_verified_from_workbook"] is False

    governance = data["rights_governance"]
    assert governance["public_catalogue_visibility_is_reuse_permission"] is False
    assert governance["catalogue_metadata_is_verified_workbook_content"] is False
    assert governance["statistical_table_is_cultural_authorization"] is False
    assert governance["community_validation_inferred"] is False

    assert data["canonicalization"]["controlled_identity_count_changed"] is False
