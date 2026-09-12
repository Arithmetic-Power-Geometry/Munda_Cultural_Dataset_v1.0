import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lexibank_peiros_mundari_formtable_rowcount_run269_2026-09-12.json"
LOG = ROOT / "data/source_census/search_log_run269.jsonl"


def test_run269_peiros_mundari_cardinality_and_pin():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["source"]["release_tag"] == "v1.1"
    assert d["source"]["tag_commit_sha"] == "b4d2e4dcee173494c90328f7cafd78c9851c0956"
    assert d["source"]["forms_git_blob_sha"] == "28f882e317c2caeb8c112e3b60ae2d8c1c8b9ab5"
    assert d["exact_selector_audit"]["selector"] == "Language_ID == Mundari"
    assert d["exact_selector_audit"]["matches_in_pinned_blob"] == 202


def test_run269_sample_locators_are_exact_and_no_bulk_promotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    rows = d["sample_exact_row_locators"]
    assert len(rows) == 21
    assert rows[0]["ID"] == "Mundari-1_all-1"
    assert rows[-1]["ID"] == "Mundari-21_ear-1"
    assert all(r["Language_ID"] == "Mundari" for r in rows)
    assert all(r["Source"] == "Peiros2004a" for r in rows)
    assert d["rights_and_cultural_boundary"]["controlled_lexical_rows_promoted"] == 0
    assert d["rights_and_cultural_boundary"]["participant_consent_inferred"] is False
    assert d["rights_and_cultural_boundary"]["community_validation_inferred"] is False
    assert d["rights_and_cultural_boundary"]["cultural_access_permission_inferred"] is False


def test_run269_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000269" for r in rows)
