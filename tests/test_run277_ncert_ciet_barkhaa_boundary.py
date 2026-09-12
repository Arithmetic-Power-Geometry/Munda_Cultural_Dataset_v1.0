import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/ncert_ciet_barkhaa_mundari_audio_locator_run277_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run277.jsonl"


def test_run277_exact_first_party_locator_and_titles():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["source"]["institution"].startswith("Central Institute of Educational Technology")
    assert d["source"]["url"] == "https://ciet.ncert.gov.in/barkhaa_audio"
    assert d["source"]["verified_level1_titles_with_mundari"] == 9
    titles = {x["title"] for x in d["source"]["mundari_exact_title_locators"]}
    assert titles == {
        "Chhupan Chhupaai", "Gilli Danda", "Mzza Aa Gya", "Milli ka Gubbara",
        "Mithai", "Mithe Mithe Gulgule", "Munmun Aur Munnu", "Phooli Roti", "Rani Bhi"
    }


def test_run277_no_unsupported_audio_or_cultural_promotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    p = d["promotion"]
    b = d["rights_and_cultural_boundary"]
    assert p["audio_bytes_promoted"] == 0
    assert p["transcript_rows_promoted"] == 0
    assert p["claims_added"] == 0
    assert p["evidence_records_added"] == 0
    assert p["cultural_claims_promoted"] == 0
    assert b["public_page_treated_as_redistribution_permission"] is False
    assert b["participant_or_performer_consent_verified"] is False
    assert b["community_validation_verified"] is False
    assert b["cultural_access_permission_verified"] is False


def test_run277_count_change_is_blocked_until_dedup_reconciliation():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["canonicalization"]["canonical_key"] == "CIET-NCERT:BARKHAA-AUDIO:MUNDARI"
    assert d["canonicalization"]["count_change_allowed"] is False
    assert d["promotion"]["controlled_source_identity_count_change"] is False


def test_run277_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert len(rows) == 14
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000277" for r in rows)
