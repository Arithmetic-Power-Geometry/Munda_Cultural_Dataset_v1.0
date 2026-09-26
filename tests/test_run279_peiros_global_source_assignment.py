import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lexibank_peiros_global_source_assignment_run279_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run279.jsonl"


def test_run279_pinned_generator_and_source_assignment():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["source"]["release_tag"] == "v1.1"
    assert d["source"]["tag_commit_sha"] == "b4d2e4dcee173494c90328f7cafd78c9851c0956"
    assert d["source"]["generator_git_blob_sha"] == "544d81c37b5a6bdbf3e4a1e7a10a463d47474282"
    assert d["source"]["mundari_form_rows_total"] == 101
    s = d["structural_verification"]
    assert s["form_generation_source_argument"] == ["Peiros2004a"]
    assert s["cognate_generation_source_argument"] == ["Peiros2004a"]
    assert s["source_key_provenance_unresolved_after_run279"] == 0
    assert s["exact_row_parameter_locator_reconciliation_remaining"] == 80
    assert s["bulk_lexical_promotion_complete"] is False


def test_run279_no_unsupported_promotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    p = d["promotion"]
    assert p["controlled_source_identity_count_change"] is False
    assert p["controlled_lexical_rows_promoted"] == 0
    assert p["claims_added"] == 0
    assert p["evidence_records_added"] == 0
    assert p["evidence_links_added"] == 0
    assert p["cultural_claims_promoted"] == 0
    b = d["rights_and_cultural_boundary"]
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False


def test_run279_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert len(rows) == 14
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000279" for r in rows)
