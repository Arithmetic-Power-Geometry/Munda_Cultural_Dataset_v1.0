import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "tri_jharkhand_mundari_publication_register_run257_2026-09-12.json"
LOG = ROOT / "data" / "source_census" / "search_log_run257.jsonl"


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run257_exact_official_tri_register_entries():
    d = load_audit()
    assert d["run_id"] == 257
    rows = {row["register_serial"]: row for row in d["verified_register_entries"]}
    assert set(rows) == {1, 2, 14, 19, 88}
    assert rows[1]["title_as_displayed"] == "Mundari - Hindi Sabdhkosh"
    assert rows[2]["title_as_displayed"] == "Hindi - Mundari Sabdhkosh"
    assert rows[14]["title_as_displayed"] == "Mundari Vartalap Nirdeshika"
    assert rows[19]["title_as_displayed"] == "Munda"
    assert rows[19]["year_as_displayed"] == "1993"
    assert rows[88]["title_as_displayed"] == "Anayum Durang (Mundari folk song)"


def test_run257_access_and_rights_are_not_overread():
    d = load_audit()
    boundary = d["rights_access_consent_cultural_boundary"]
    promotion = d["promotion"]
    assert boundary["official_catalogue_metadata_verified"] is True
    assert boundary["catalogue_visibility_treated_as_redistribution_permission"] is False
    assert boundary["download_link_treated_as_reuse_permission"] is False
    assert boundary["downloadable_bytes_acquired"] is False
    assert boundary["cryptographic_hash_verified"] is False
    assert boundary["redistribution_permission_verified"] is False
    assert boundary["model_training_permission_verified"] is False
    assert boundary["participant_or_performer_consent_verified"] is False
    assert boundary["community_validation_verified"] is False
    assert boundary["cultural_access_permission_verified"] is False
    assert boundary["folk_song_cultural_sensitivity_review_required"] is True
    assert promotion["discovery_only"] is False
    assert promotion["catalogue_evidence_records_promoted"] == 5
    assert promotion["content_evidence_promoted"] is False
    assert promotion["lexical_rows_promoted"] == 0
    assert promotion["song_text_or_audio_promoted"] == 0
    assert promotion["cultural_claims_promoted"] == 0


def test_run257_blocked_downloads_remain_explicit_gaps():
    d = load_audit()
    blocked = {row["drive_file_id"] for row in d["blocked_attempts"]}
    assert blocked == {
        "13ZOOkv-KVrKixzpqWAHj61ZpdiH4uMfb",
        "19MJ3iIgRC33GoqruLWMPDb57PukIweSB",
    }
    assert d["deduplication"]["identity_count_change"] is False
    assert any("73 unresolved" in gap for gap in d["explicit_gaps"])


def test_run257_search_log_covers_all_required_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {row["class"] for row in rows}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert classes == expected
    assert all(row["search_id"] == "MMSC-SEARCH-000257" for row in rows)
