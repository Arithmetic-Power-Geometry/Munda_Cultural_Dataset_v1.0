import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/bangladesh_multiling_munda_archive_exact_locator_run273_2026-09-13.json"
LOG = ROOT / "data/source_census/search_log_run273.jsonl"


def test_run273_exact_official_locator_and_cardinality():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    s = d["source"]
    assert s["canonical_url"] == "https://lob.bangla.gov.bd/languages/munda"
    assert s["full_archive_units_displayed"] == 860
    assert s["archive_index_sentences_displayed"] == 860
    assert s["archive_index_minutes_displayed"] == 280
    assert s["rights_notice"] == "© 2026 BCC - ICTD. All rights reserved."


def test_run273_scope_and_rights_boundary():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["scope_classification"]["mlhkp_core_geography"] is False
    b = d["rights_and_cultural_boundary"]
    assert b["public_access_treated_as_redistribution_permission"] is False
    assert b["model_training_permission_inferred"] is False
    assert b["participant_consent_inferred"] is False
    assert b["community_validation_inferred"] is False
    assert b["cultural_access_permission_inferred"] is False
    assert b["audio_units_promoted"] == 0
    assert b["transcription_rows_promoted"] == 0
    assert b["controlled_cultural_claims_promoted"] == 0


def test_run273_count_neutral_until_deterministic_reconciliation():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["deduplication"]["canonical_key"] == "gov-bd:multiling-cloud:munda"
    assert d["deduplication"]["identity_count_change"] is False
    assert d["promotion"]["controlled_claim_rows_added"] == 0
    assert d["promotion"]["controlled_evidence_rows_added"] == 0
    assert d["promotion"]["controlled_evidence_links_added"] == 0


def test_run273_search_log_covers_all_controlled_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert len(rows) == 14
    assert {r["class"] for r in rows} == expected
    assert all(r["search_id"] == "MMSC-SEARCH-000273" for r in rows)
