import json
from pathlib import Path


def test_run309_c17_exact_locator_boundary():
    path = Path("data/source_census/census_c17_jharkhand_exact_schema_locator_run309_2026-09-13.json")
    obj = json.loads(path.read_text(encoding="utf-8"))

    assert obj["canonical_source"]["reference_id"] == "PC11_C17-20"
    assert obj["canonical_source"]["declared_download_filename"] == "DDW-C17-2000.XLSX"
    assert obj["canonical_source"]["geographic_code"] == "20"

    locators = set(obj["exact_schema_locators"])
    required = {
        "Language - Total speakers - MUNDA",
        "Language - Total speakers - MUNDARI",
        "1st subsidiary language - MUNDA",
        "1st subsidiary language - MUNDARI",
        "2nd subsidiary language - MUNDA",
        "2nd subsidiary language - MUNDARI",
    }
    assert required <= locators

    verification = obj["verification"]
    assert verification["official_catalogue_identity_verified"] is True
    assert verification["official_declared_filename_verified"] is True
    assert verification["xlsx_bytes_independently_acquired"] is False
    assert verification["xlsx_sha256_independently_computed"] is False
    assert verification["sheet_inventory_verified"] is False
    assert verification["exact_numeric_cells_verified"] is False
    assert verification["numeric_values_promoted"] is False

    promotion = obj["evidence_promotion"]
    assert promotion["new_controlled_cultural_claims"] == 0
    assert promotion["new_controlled_numeric_claims"] == 0
    assert promotion["new_evidence_records"] == 0
    assert promotion["new_provenance_links"] == 0
    assert promotion["count_neutral"] is True

    governance = obj["rights_and_governance"]
    assert governance["participant_consent_inferred"] is False
    assert governance["community_validation_inferred"] is False
    assert governance["cultural_access_permission_inferred"] is False
