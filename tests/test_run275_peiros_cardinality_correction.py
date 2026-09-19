import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lexibank_peiros_cardinality_correction_run275_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run275.jsonl"


def test_run275_corrects_connector_double_count():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    c = d["correction"]
    assert d["source"]["release_tag"] == "v1.1"
    assert d["source"]["tag_commit_sha"] == "b4d2e4dcee173494c90328f7cafd78c9851c0956"
    assert d["source"]["forms_git_blob_sha"] == "28f882e317c2caeb8c112e3b60ae2d8c1c8b9ab5"
    assert c["previous_reported_mundari_matches"] == 202
    assert c["correct_distinct_csv_rows"] == 101
    assert c["verification"]["mundari_hits_in_single_csv_representation"] == 101
    assert c["verification"]["mundari_hits_in_full_connector_resource"] == 202
    assert c["verification"]["connector_representation_multiplier"] == 2
    assert c["sample_reconciliation_rows_already_verified"] == 21
    assert c["correct_unreconciled_rows_remaining"] == 80
    assert c["bulk_reconciliation_complete"] is False


def test_run275_second_form_rows_and_parameter_table_are_bounded():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    v = d["correction"]["verification"]
    assert v["parameter_table_keys"] == 100
    assert v["second_form_row_hits_suffix_2"] == 3
    assert v["second_form_row_ids_verified"] == [
        "Mundari-3_bark-2", "Mundari-39_hear-2", "Mundari-93_warm-2"
    ]
    assert v["source_key_exists_in_pinned_sources_bib"] is True
    assert v["parameter_table_pinned_and_verified"] is True


def test_run275_no_unsupported_content_promotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    b = d["rights_and_cultural_boundary"]
    assert b["controlled_lexical_rows_promoted"] == 0
    assert b["controlled_cultural_claims_promoted"] == 0
    assert b["underlying_source_blanket_permission_inferred"] is False
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False


def test_run275_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert len(rows) == 14
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000275" for r in rows)
