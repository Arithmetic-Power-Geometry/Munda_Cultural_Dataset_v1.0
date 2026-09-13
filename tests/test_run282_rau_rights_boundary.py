import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/rau_zenodo_rights_integrity_audit_run282_2026-09-13.json"
SEARCH = ROOT / "data/source_census/search_log_run282.jsonl"


def test_run282_rau_rights_integrity_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    src = data["source"]
    assert src["zenodo_record"] == "3380874"
    assert src["doi"] == "10.5281/zenodo.3380874"
    assert src["repository_declared_md5"] == "07e1d945a0fc6cafc4fc7afd3f1ff144"
    assert src["repository_description_cognate_count"] == 127
    assert src["mundari_explicitly_listed"] is True
    assert src["license"] == "CC0-1.0"
    verify = data["verification"]
    assert verify["independent_byte_acquisition_this_run"] is False
    assert verify["independent_md5_recomputed_this_run"] is False
    assert verify["row_level_source_attribution_complete"] is False
    rights = data["rights_and_cultural_boundary"]
    assert rights["license_treated_as_participant_consent"] is False
    assert rights["license_treated_as_community_validation"] is False
    assert rights["license_treated_as_cultural_access_permission"] is False
    assert rights["cultural_access_overrides_legal_or_technical_entitlement"] is True
    assert data["promotion"]["controlled_claims_added"] == 0
    assert data["promotion"]["cultural_claims_promoted"] == 0


def test_run282_search_log_covers_all_required_classes():
    records = [json.loads(line) for line in SEARCH.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(records) == 14
    assert {r["class"] for r in records} == {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media"
    }
