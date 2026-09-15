import json
from pathlib import Path

AUDIT = Path("data/source_census/koshy_2024_munda_multiverb_mundari_exact_locator_run306_2026-09-13.json")
LOG = Path("data/source_census/search_log_run306.jsonl")


def test_run306_koshy_exact_locator_and_governance_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["run_id"] == 306
    assert data["canonical_source"]["doi"] == "10.54392/ijll2436"
    assert data["canonical_source"]["license"] == "CC BY 4.0"
    assert data["canonical_source"]["pages"] == "62-75"
    pages = [x["printed_page"] for x in data["mundari_scope_exact_locators"]]
    assert pages == [62, 63, 64]
    assert data["rights_and_governance_boundary"]["fieldwork_material_promoted"] is False
    assert data["rights_and_governance_boundary"]["license_treated_as_participant_consent"] is False
    assert data["rights_and_governance_boundary"]["license_treated_as_community_validation"] is False
    assert data["rights_and_governance_boundary"]["license_treated_as_cultural_access_permission"] is False
    assert data["promotion"]["new_controlled_cultural_claims"] == 0
    assert data["promotion"]["new_controlled_lexical_rows"] == 0
    assert data["promotion"]["new_controlled_evidence_records"] == 0
    assert data["promotion"]["new_evidence_links"] == 0
    assert data["promotion"]["count_bearing_source_identity_change"] is False
    assert data["deduplication"]["unresolved_WEB_MUN_count_decrement"] == 0


def test_run306_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI materials", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio", "video",
        "maps", "relevant media"
    }
    assert {row["class"] for row in rows} == expected
    peer = next(row for row in rows if row["class"] == "peer-reviewed articles")
    assert peer["result"] == "promoted-exact-locator"
    assert "10.54392/ijll2436" in peer["note"]
