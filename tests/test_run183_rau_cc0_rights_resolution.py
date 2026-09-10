import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/rau_2019_cc0_rights_resolution_run183_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run183.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_rau_cc0_exact_rights_locator_and_boundaries():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["run"] == 183
    assert d["branch"] == "mlhkp-v2"
    assert d["source"]["doi"] == "10.5281/zenodo.3380874"
    assert d["authoritative_exact_locators"]["license_identifier"] == "CC0-1.0"
    assert d["authoritative_exact_locators"]["license_value_authoritatively_verified"] is True
    assert d["manifestation_and_hash"]["independent_md5_recomputed"] is False
    assert d["manifestation_and_hash"]["repository_md5_promoted_as_independent"] is False
    assert d["rights_and_cultural_access"]["participant_consent_inferred"] is False
    assert d["rights_and_cultural_access"]["community_validation_inferred"] is False
    assert d["rights_and_cultural_access"]["cultural_access_permission_inferred"] is False
    assert d["evidence_boundary"]["dataset_rows_ingested_run183"] is False
    assert d["evidence_boundary"]["cultural_claims_ingested_run183"] is False
    assert d["deduplication"]["new_permanent_source_identity_assigned"] is False
    assert d["deduplication"]["count_bearing_change"] is False


def test_run183_federated_class_coverage():
    rows = [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines() if x.strip()]
    classes = {x["class"] for x in rows}
    expected = {
        "books_dictionaries_grammars", "peer_reviewed_articles", "theses_dissertations",
        "government_tri_census_lsi", "archives", "newspapers_periodicals", "web_resources",
        "datasets", "audio", "video", "maps", "relevant_media"
    }
    assert expected <= classes
    assert {x["search_id"] for x in rows} == {"MMSC-SEARCH-000183"}


def test_run183_status_count_contract():
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    assert s["latest_run"] == 183
    assert s["branch"] == "mlhkp-v2"
    assert s["mmsc"]["audited_source_identities"] == 42
    assert s["mmsc"]["raw_web_discovery_records"] == 90
    assert s["mmsc"]["unique_web_discovery_leads"] == 87
    assert s["mmsc"]["duplicate_web_records"] == 3
    assert s["mmsc"]["canonicalized_unique_web_leads"] == 14
    assert s["mmsc"]["unresolved_unique_web_leads"] == 73
    assert s["evidence_and_schema"]["source_claims"] == 52
    assert s["evidence_and_schema"]["evidence_records"] == 52
    assert s["evidence_and_schema"]["evidence_links"] == 52
    assert s["streamlit"]["registered_modules"] == 42
    assert s["streamlit"]["mapped_modules"] == 42
    assert s["rights_governance"]["rau_exact_license_value_verified"] is True
    assert s["rights_governance"]["rau_row_level_reuse_permitted"] is False
    assert s["release_gate"]["status"] == "NOT_PASS"
