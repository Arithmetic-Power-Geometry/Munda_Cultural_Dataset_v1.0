import json
from pathlib import Path


def test_run347_asjp_promotion_boundary():
    p = Path("data/source_census/asjp_mundari_exact_locator_run347_2026-09-14.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    v = d["verification"]
    assert d["identity"]["iso_639_3"] == "unr"
    assert d["identity"]["glottocode"] == "mund1320"
    assert v["provider_page_identity_verified"] is True
    assert v["license_statement_verified_on_provider_page"] is True
    assert v["export_bytes_downloaded_and_hashed"] is False
    assert v["export_row_count_recomputed"] is False
    assert v["individual_lexical_items_independently_verified"] is False
    assert v["community_validation_verified"] is False
    assert v["cultural_access_authorization_inferred"] is False
    assert d["deduplication"]["count_change_authorized"] is False


def test_run347_search_log_covers_all_controlled_classes():
    p = Path("audits/mmsc_search_run347_2026-09-14.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["classes_refreshed"] == 14
    assert len(d["classes"]) == 14
    assert d["controlled_counts_changed"] is False
