import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "shrivastava_2013_mundari_khuntkatti_exact_locator_run259_2026-09-12.json"
LOG = ROOT / "data" / "source_census" / "search_log_run259.jsonl"


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_run259_exact_peer_reviewed_identity_and_locator():
    d = load_audit()
    assert d["run_id"] == 259
    src = d["source"]
    assert src["doi"] == "10.1177/0972558X1301300205"
    assert src["journal"] == "The Oriental Anthropologist"
    assert src["volume"] == 13
    assert src["issue"] == 2
    assert src["pages"] == "267-280"
    assert src["first_published_online"] == "2013-07-01"
    assert any(x["locator_type"] == "publisher_abstract" for x in d["exact_locators"])


def test_run259_existing_discovery_is_canonicalized_not_double_counted():
    d = load_audit()
    dedup = d["deduplication"]
    assert dedup["canonical_key"] == "doi:10.1177/0972558X1301300205"
    assert dedup["identity_count_change"] is False
    assert "Run 257" in dedup["prior_repository_state"]


def test_run259_rights_consent_and_cultural_boundaries_hold():
    d = load_audit()
    b = d["rights_access_consent_cultural_boundary"]
    p = d["promotion"]
    assert b["publisher_metadata_and_abstract_publicly_rendered"] is True
    assert b["public_abstract_treated_as_blanket_permission"] is False
    assert b["full_text_reuse_license_verified"] is False
    assert b["redistribution_permission_verified"] is False
    assert b["model_training_permission_verified"] is False
    assert b["participant_consent_independently_verified"] is False
    assert b["community_validation_verified"] is False
    assert b["cultural_access_permission_verified"] is False
    assert p["discovery_only"] is False
    assert p["full_text_passages_promoted"] == 0
    assert p["legal_or_land_tenure_claims_promoted"] == 0
    assert p["cultural_claims_promoted"] == 0
    assert p["participant_derived_records_promoted"] == 0
    assert p["evidence_claim_count_change"] is False


def test_run259_blocked_lsi_attempt_is_not_promoted():
    d = load_audit()
    blocked = d["blocked_attempts"]
    assert len(blocked) == 1
    assert blocked[0]["source"] == "Linguistic Survey of India - Jharkhand"
    assert "502" in blocked[0]["observation"]
    assert "do not promote" in blocked[0]["disposition"]


def test_run259_search_log_covers_all_required_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {row["class"] for row in rows}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert classes == expected
    assert len(rows) == 14
    assert all(row["search_id"] == "MMSC-SEARCH-000259" for row in rows)
