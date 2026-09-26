import json
from pathlib import Path


def test_run367_map_is_locator_not_primary_census_evidence():
    path = Path("audits/wikimedia_mundari_assam_map_exact_locator_run367_2026-09-15.json")
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["promotion_state"] == "exact_provider_manifestation_locator_and_license_only"
    assert data["license"] == "CC BY-SA 4.0"
    assert "C-16" in data["declared_data_source"]
    assert data["count_effect"] == "none"
    assert data["claim_effect"] == "none"

    blocked = set(data["not_promoted"])
    assert "district-level Mundari speaker counts" in blocked
    assert "map-derived demographic values" in blocked
    assert "independent verification of the underlying C-16 workbook" in blocked


def test_run367_census_refresh_preserves_controlled_counts():
    path = Path("audits/mmsc_refresh_run367_2026-09-15.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    counts = data["controlled_counts"]

    assert data["controlled_classes_refreshed"] == 14
    assert data["count_change_this_run"] is False
    assert counts == {
        "audited_source_identities": 42,
        "raw_web_discovery_records": 90,
        "unique_web_discovery_leads": 87,
        "duplicate_web_records": 3,
        "canonicalized_unique_web_leads": 14,
        "unresolved_unique_web_leads": 73,
    }
