import json
from pathlib import Path


AUDIT = Path("data/source_census/lexibank_lsi_mundari_exact_row_locator_run286_2026-09-13.json")
LOG = Path("data/source_census/search_log_run286.jsonl")


def _audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run286_pinned_identity_and_counts():
    d = _audit()
    assert d["run_id"] == 286
    assert d["source"]["pinned_commit_sha"] == "bfae847565dc6810af05c11bf612457e5861009e"
    assert d["source"]["language_id"] == "MUNDARI"
    assert d["source"]["glottocode"] == "mund1320"
    rows = d["verified_exact_rows"]
    assert len(rows) == 10
    assert len({r["computed_id"] for r in rows}) == 10
    assert len({r["Parameter_ID"] for r in rows}) == 10
    assert d["verification"]["cumulative_exact_computed_rows_verified_across_runs_281_283_285_286"] == 27
    assert d["verification"]["cumulative_distinct_parameter_ids_verified_across_runs_281_283_285_286"] == 22


def test_run286_exact_foreign_key_examples():
    d = _audit()
    by_id = {r["computed_id"]: r for r in d["verified_exact_rows"]}
    assert by_id["57450"]["Parameter_ID"] == "57_cat"
    assert by_id["57450"]["CONCEPTICON"] == "1208"
    assert by_id["57450"]["parameter_locator"]["scan_numbers"] == "156 157"
    assert by_id["30477"]["Parameter_ID"] == "121_come"
    assert by_id["30477"]["CONCEPTICON"] == "1446"
    assert by_id["31245"]["Parameter_ID"] == "123_die"
    assert by_id["31245"]["parameter_locator"]["primary_lsi_page_numbers"] == "246-247"


def test_run286_primary_and_governance_boundary():
    d = _audit()
    assert d["verification"]["direct_primary_page_image_verified_this_run"] is False
    assert d["verification"]["direct_primary_scan_bytes_hashed_this_run"] is False
    assert d["promotion"]["controlled_claims_added"] == 0
    assert d["promotion"]["controlled_evidence_records_added"] == 0
    assert d["promotion"]["cultural_claims_promoted"] == 0
    assert d["rights_and_cultural_boundary"]["derived_license_treated_as_primary_scan_permission"] is False
    assert d["rights_and_cultural_boundary"]["community_validation_inferred"] is False
    assert d["rights_and_cultural_boundary"]["cultural_access_permission_inferred"] is False


def test_run286_all_fourteen_classes_logged_once():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = [r["class"] for r in rows]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles", "theses_dissertations",
        "government_TRI_Census_LSI", "archives", "newspapers_periodicals", "web_resources",
        "datasets", "audio", "video", "maps", "relevant_media"
    }
    assert len(rows) == 14
    assert set(classes) == expected
    assert len(classes) == len(set(classes))
