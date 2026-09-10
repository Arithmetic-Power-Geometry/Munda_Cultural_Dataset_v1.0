import json
from pathlib import Path


def test_run177_kumari_rahman_identity_rights_and_boundary():
    p = Path("data/source_census/kumari_rahman_2021_livelihood_exact_locator_run177_2026-09-11.json")
    audit = json.loads(p.read_text(encoding="utf-8"))
    assert audit["run"] == 177
    assert audit["source_identity"]["doi"] == "10.35784/pe.2021.1.19"
    assert audit["source_identity"]["pages"] == "181-185"
    assert audit["source_identity"]["identity_verified"] is True
    assert audit["rights_governance"]["publisher_stated_license"] == "CC BY-SA 4.0"
    assert audit["scope_classification"]["population_wide_generalization_permitted"] is False
    assert audit["rights_governance"]["participant_consent_inferred"] is False
    assert audit["rights_governance"]["community_validation_inferred"] is False
    assert audit["rights_governance"]["cultural_access_permission_inferred"] is False
    assert audit["promotion_decision"]["cultural_claims_added"] == 0
    assert audit["promotion_decision"]["participant_records_ingested"] == 0
    assert audit["promotion_decision"]["count_change"] == 0


def test_run177_search_log_covers_requested_classes():
    row = json.loads(Path("data/source_census/search_log_run177.jsonl").read_text(encoding="utf-8").strip())
    classes = {r["class"] for r in row["results"]}
    required = {"books", "dictionaries", "grammars", "peer_reviewed_articles", "theses_dissertations", "government_TRI_Census_LSI", "archives", "newspapers", "web_resources", "datasets", "audio", "video", "maps", "relevant_media"}
    assert required <= classes
    assert row["count_change"] == 0
    assert row["claims_added"] == 0
    assert row["evidence_added"] == 0
