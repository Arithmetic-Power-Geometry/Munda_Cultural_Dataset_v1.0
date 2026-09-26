import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "whitley_1873_mundari_primer_exact_locator_run255_2026-09-12.json"
LOG = ROOT / "data" / "source_census" / "search_log_run255.jsonl"


def load_audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_whitley_exact_identity_and_persistent_locator():
    d = load_audit()
    assert d["run_id"] == 255
    assert d["work"]["canonical_title"] == "A Mundári Primer"
    assert d["work"]["author"] == "J. C. Whitley"
    assert d["work"]["year"] == 1873
    ddb = d["verified_locators"][0]
    assert ddb["urn"] == "urn:nbn:de:bvb:12-bsb11159896-3"
    assert ddb["holding_shelfmark"].endswith("L.as. 386 n")
    assert ddb["extent"] == "3 Bl. 35 S."


def test_whitley_rights_and_content_boundary_is_non_inferential():
    d = load_audit()
    rights = d["rights_access_boundary"]
    promotion = d["promotion"]
    assert "Nur nicht kommerzielle Nutzung erlaubt" in rights["ddb_displayed_rights"]
    assert rights["complete_digitized_bytes_acquired"] is False
    assert rights["cryptographic_hash_verified"] is False
    assert rights["redistribution_permission_verified_for_mlhkp"] is False
    assert rights["model_training_permission_verified"] is False
    assert rights["participant_consent_verified"] is False
    assert rights["community_validation_verified"] is False
    assert rights["cultural_access_permission_verified"] is False
    assert promotion["content_evidence_promoted"] is False
    assert promotion["lexical_rows_promoted"] == 0
    assert promotion["grammatical_propositions_promoted"] == 0
    assert promotion["cultural_claims_promoted"] == 0


def test_run255_is_count_neutral_until_full_lead_reconciliation():
    d = load_audit()
    dedup = d["deduplication"]
    assert dedup["identity_count_change"] is False
    assert "73 unresolved" in d["explicit_gaps"][-1]


def test_run255_search_log_covers_all_required_classes():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    classes = {row["class"] for row in rows}
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert classes == expected
    assert all(row["search_id"] == "MMSC-SEARCH-000255" for row in rows)
