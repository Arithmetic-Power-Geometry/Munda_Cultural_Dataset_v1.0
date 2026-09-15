import json
from pathlib import Path

AUDIT = Path("data/source_census/bera_2026_munda_identity_audit_run327_2026-09-14.json")
SEARCH_LOG = Path("data/source_census/search_log_run327.jsonl")


def test_run327_peer_reviewed_article_without_fieldwork_overpromotion():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["source_class"] == "peer-reviewed articles"
    assert d["doi"] == "10.1177/2455328X261437865"
    assert d["source_observations"]["peer_reviewed_article_identity_verified"] is True
    assert d["source_observations"]["full_article_bytes_independently_acquired"] is False
    assert d["source_observations"]["underlying_primary_fieldwork_dataset_acquired"] is False
    assert d["governance"]["participant_consent_inferred"] is False
    assert d["governance"]["community_validation_inferred"] is False
    assert d["governance"]["cultural_access_authorization_inferred"] is False
    assert d["governance"]["fieldwork_content_promoted"] is False
    assert d["promotion"]["new_controlled_source_identity"] is False
    assert d["promotion"]["new_controlled_claim"] is False
    assert d["promotion"]["new_evidence_record"] is False
    assert d["promotion"]["new_evidence_link"] is False


def test_run327_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in SEARCH_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer-reviewed articles", "theses/dissertations",
        "government/TRI/Census/LSI", "archives", "newspapers", "web resources", "datasets",
        "audio", "video", "maps", "relevant media"
    }
    assert len(rows) == 14
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000327" for r in rows)
    assert all(r["promoted"] is False for r in rows)
