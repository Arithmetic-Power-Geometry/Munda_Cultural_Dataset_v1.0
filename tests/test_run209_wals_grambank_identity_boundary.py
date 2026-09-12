import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/wals_grambank_mundari_identity_boundary_run209_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run209.jsonl"


def test_run209_wals_grambank_identity_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    loc = data["locators"]
    ver = data["verification"]
    dedup = data["deduplication"]
    assert data["run"] == 209
    assert loc["wals_mundari"]["wals_code"] == "mun"
    assert loc["wals_mundari"]["iso_639_3"] == "unr"
    assert loc["wals_bhumij"]["wals_code"] == "bhu"
    assert loc["wals_bhumij"]["glottocode_displayed"] == "mund1320"
    assert loc["grambank_mundari"]["glottocode"] == "mund1320"
    assert loc["grambank_datapoint_example"]["feature_id"] == "GB317"
    assert ver["underlying_grammar_pages_directly_verified"] is False
    assert ver["typological_value_promoted_as_public_claim"] is False
    assert ver["count_bearing_registration_performed"] is False
    assert dedup["wals_mundari_and_bhumij_collapsed"] is False
    assert dedup["grambank_and_wals_collapsed_into_one_source_identity"] is False
    assert data["rights_access_governance"]["community_validation_inferred"] is False
    assert data["rights_access_governance"]["cultural_access_permission_inferred"] is False
    assert data["evidence_promotion"]["new_cultural_claims"] == 0


def test_run209_all_requested_source_classes_logged():
    row = json.loads(LOG.read_text(encoding="utf-8").strip())
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles",
        "theses/dissertations", "government/TRI/Census/LSI", "archives",
        "newspapers/periodicals", "web resources", "datasets", "audio",
        "video", "maps", "relevant media"
    }
    assert row["search_id"] == "MMSC-SEARCH-000209"
    assert expected.issubset(set(row["classes"]))
    assert row["counts_changed"] is False
    assert row["cultural_claims_added"] == 0
    assert any("WALS Bhumij" in note for note in row["identity_boundary"])
