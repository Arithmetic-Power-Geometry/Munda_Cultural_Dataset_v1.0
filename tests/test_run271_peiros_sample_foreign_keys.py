import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lexibank_peiros_sample_foreign_key_reconciliation_run271_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run271.jsonl"


def test_run271_peiros_sample_foreign_key_reconciliation():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["source"]["release_tag"] == "v1.1"
    assert d["source"]["tag_commit_sha"] == "b4d2e4dcee173494c90328f7cafd78c9851c0956"
    assert d["source"]["sources_git_blob_sha"] == "0629a9d2536b09f6c615aa33c471a6550e274acd"
    assert d["source"]["parameters_git_blob_sha"] == "f13b1827b4ee61f6f38b5031afe7a7d5fa027692"
    s = d["sample_reconciliation"]
    assert s["sample_rows"] == 21
    assert s["source_key_verified_rows"] == 21
    assert s["parameter_key_verified_rows"] == 21
    assert s["unresolved_rows_remaining"] == 181
    assert s["bulk_202_row_reconciliation_complete"] is False


def test_run271_exact_source_and_parameter_keys():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["source_foreign_key"]["key"] == "Peiros2004a"
    assert d["source_foreign_key"]["year"] == 2004
    rows = d["rows"]
    assert len(rows) == 21
    assert all(r["Source"] == "Peiros2004a" for r in rows)
    assert rows[0]["Parameter_ID"] == "1_all"
    assert rows[0]["Concepticon_ID"] == "98"
    assert rows[-1]["Parameter_ID"] == "21_ear"
    assert rows[-1]["Concepticon_ID"] == "1247"


def test_run271_no_unsupported_content_promotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    b = d["rights_and_cultural_boundary"]
    assert b["controlled_lexical_rows_promoted"] == 0
    assert b["controlled_cultural_claims_promoted"] == 0
    assert b["underlying_source_blanket_permission_inferred"] is False
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False


def test_run271_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert len(rows) == 14
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000271" for r in rows)
