import json
from pathlib import Path


def test_run336_census_regional_locator_boundary():
    p = Path("data/source_census/census_2011_c16_regional_locator_run336_2026-09-14.json")
    data = json.loads(p.read_text(encoding="utf-8"))

    assert data["run"] == 336
    assert data["source_class"] == "government_Census"
    assert len(data["records"]) == 3

    expected = {
        "Jharkhand": ("PC11_C16-20", "DDW-C16-STMT-MDDS-2000.xlsx"),
        "West Bengal": ("PC11_C16-19", "DDW-C16-STMT-MDDS-1900.xlsx"),
        "Odisha": ("PC11_C16-21", "DDW-C16-STMT-MDDS-2100.xlsx"),
    }

    for record in data["records"]:
        ref_id, filename = expected[record["region"]]
        assert record["reference_id"] == ref_id
        assert record["file"] == filename
        assert record["locator_verified"] is True
        assert record["workbook_bytes_verified"] is False
        assert record["hash_verified"] is False
        assert record["sheet_and_cell_locators_verified"] is False

    assert data["promotion"]["exact_catalog_and_filename_locators"] is True
    assert data["promotion"]["numerical_cells_promoted"] is False
    assert data["promotion"]["controlled_counts_changed"] is False
