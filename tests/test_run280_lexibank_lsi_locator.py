import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/lexibank_lsi_mundari_language_locator_run280_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run280.jsonl"


def test_run280_pinned_lsi_mundari_locator():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["source"]["pinned_commit_sha"] == "bfae847565dc6810af05c11bf612457e5861009e"
    v = d["verified_locator"]
    assert v["Language_ID"] == "MUNDARI"
    assert v["Glottocode"] == "mund1320"
    assert v["ISO639P3code"] == "unr"
    assert v["NumberInSource"] == "16."
    assert v["SubGroup"] == "Munda"


def test_run280_no_unsupported_content_or_rights_promotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    p = d["promotion"]
    assert p["controlled_source_identity_count_change"] is False
    assert p["lexical_rows_promoted"] == 0
    assert p["claims_added"] == 0
    assert p["evidence_records_added"] == 0
    assert p["evidence_links_added"] == 0
    assert p["cultural_claims_promoted"] == 0
    b = d["rights_and_cultural_boundary"]
    assert b["derived_license_treated_as_primary_scan_blanket_permission"] is False
    assert b["derived_license_treated_as_participant_consent"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False


def test_run280_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert len(rows) == 14
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000280" for r in rows)
