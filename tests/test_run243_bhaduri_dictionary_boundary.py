import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/bhaduri_mundari_english_dictionary_exact_locator_run243_2026-09-12.json"
LOG = ROOT / "data/source_census/search_log_run243.jsonl"


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_bhaduri_work_family_identity_and_manifestations():
    d = load_audit()
    assert d["run_id"] == 243
    assert d["search_id"] == "MMSC-SEARCH-000243"
    w = d["canonical_work"]
    assert w["title"] == "A Mundari-English Dictionary"
    assert w["author"] == "Manindra Bhusan Bhaduri"
    assert w["original_publication_year"] == 1931
    assert d["deduplication"]["manifestations_collapsed_to_one_work_family"] is True
    ids = {m["catalogue_id"] for m in d["verified_manifestations"]}
    assert {"BA27135864", "BA31909026", "BB09153012"}.issubset(ids)


def test_run243_does_not_overpromote_content_or_rights():
    d = load_audit()
    p = d["promotion"]
    assert p["lexical_entries_promoted"] == 0
    assert p["passage_records_promoted"] == 0
    assert p["cultural_claims_promoted"] == 0
    assert p["content_hashes_promoted"] == 0
    r = d["rights_access_governance"]
    assert r["full_text_reuse_license_verified"] is False
    assert r["public_availability_treated_as_permission"] is False
    assert r["redistribution_permission_inferred"] is False
    assert r["model_training_permission_inferred"] is False
    assert r["community_validation_inferred"] is False
    assert r["cultural_access_permission_inferred"] is False


def test_run243_metrics_stay_controlled_and_gate_open():
    d = load_audit()
    m = d["controlled_metrics_after_run"]
    assert m == {
        "audited_source_identities": 42,
        "raw_web_discovery_records": 90,
        "unique_web_discovery_leads": 87,
        "duplicate_web_records": 3,
        "canonicalized_unique_web_leads": 14,
        "unresolved_unique_web_leads": 73,
        "additional_federated_discoveries": 28,
        "still_to_acquire_additional_discoveries": 27,
        "source_claims": 52,
        "evidence_records": 52,
        "evidence_links": 52,
        "streamlit_modules": 42,
    }
    assert d["deduplication"]["count_bearing_identity_added_this_run"] is False
    assert d["release_gate"] == "NOT_PASS"


def test_run243_all_requested_classes_are_logged():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {row["class"] for row in rows}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
    assert expected.issubset(classes)
    assert all(row["search_id"] == "MMSC-SEARCH-000243" for row in rows)


def test_run243_preserves_metadata_conflict_instead_of_silently_resolving_it():
    d = load_audit()
    assert d["metadata_conflicts"]
    assert "1929" in d["metadata_conflicts"][0]
    assert "1931" in d["metadata_conflicts"][0]
