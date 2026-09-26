import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lexibank_lsi_mundari_exact_row_locator_run281_2026-09-13.json"
SEARCH = ROOT / "data/source_census/search_log_run281.jsonl"


def test_run281_exact_lsi_rows_and_boundaries():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["source"]["pinned_commit_sha"] == "bfae847565dc6810af05c11bf612457e5861009e"
    assert data["source"]["computed_git_blob_sha"] == "6b74d97032e3e228b6519aa8d597a790305dd340"
    assert data["source"]["parameters_git_blob_sha"] == "6e37638677321a4b3bf85974889f224176ebf391"
    rows = data["verified_exact_rows"]
    assert {r["computed_id"] for r in rows} == {"23276", "23277", "51846", "51847"}
    assert {r["Parameter_ID"] for r in rows} == {"114_and", "37_back"}
    assert {r["GLOTTOLOG"] for r in rows} == {"mund1320"}
    assert {r["CONCEPTICON"] for r in rows} == {"1577", "1291"}
    assert data["verification"]["exact_computed_rows_verified"] == 4
    assert data["verification"]["distinct_parameter_ids_verified"] == 2
    assert data["verification"]["direct_primary_page_image_verified_this_run"] is False
    assert data["promotion"]["controlled_claims_added"] == 0
    assert data["promotion"]["controlled_evidence_records_added"] == 0
    assert data["promotion"]["cultural_claims_promoted"] == 0
    rights = data["rights_and_cultural_boundary"]
    assert rights["derived_license_treated_as_primary_scan_permission"] is False
    assert rights["derived_license_treated_as_participant_consent"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_permission_inferred"] is False


def test_run281_search_log_covers_all_required_classes():
    records = [json.loads(line) for line in SEARCH.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {r["class"] for r in records}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert classes == expected
    assert len(records) == 14
