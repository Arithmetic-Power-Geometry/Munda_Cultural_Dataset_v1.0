import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/rau_2019_manifestation_transport_audit_run184_2026-09-11.json"
LOG = ROOT / "data/source_census/search_log_run184.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run184_rau_manifestation_is_verified_without_hash_overclaim():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["run"] == 184
    assert d["branch"] == "mlhkp-v2"
    m = d["authoritative_manifestation"]
    assert m["filename"] == "pMunda_cognate_set_2019-08-29.csv"
    assert m["repository_md5"] == "07e1d945a0fc6cafc4fc7afd3f1ff144"
    assert m["download_endpoint_returned_plaintext_csv"] is True
    assert m["mundari_column_directly_observed"] is True
    assert m["independent_byte_preserving_download_succeeded"] is False
    assert m["independent_md5_recomputed"] is False
    assert d["evidence_boundary"]["dataset_rows_ingested_run184"] is False
    assert d["evidence_boundary"]["cultural_claims_ingested_run184"] is False
    assert d["rights_and_cultural_access"]["cultural_access_permission_inferred"] is False


def test_run184_census_has_all_release_classes():
    rows = [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 12
    assert {r["search_id"] for r in rows} == {"MMSC-SEARCH-000184"}
    assert {r["class"] for r in rows} == {
        "books_dictionaries_grammars", "peer_reviewed_articles", "theses_dissertations",
        "government_tri_census_lsi", "archives", "newspapers_periodicals", "web_resources",
        "datasets", "audio", "video", "maps", "relevant_media"
    }


def test_run184_status_contract():
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    assert s["latest_run"] == 184
    assert s["branch"] == "mlhkp-v2"
    assert s["mmsc"]["audited_source_identities"] == 42
    assert s["mmsc"]["unresolved_unique_web_leads"] == 73
    assert s["evidence_and_schema"]["source_claims"] == 52
    assert s["streamlit"]["registered_modules"] == 42
    assert s["streamlit"]["mapped_modules"] == 42
    assert s["release_gate"]["status"] == "NOT_PASS"
