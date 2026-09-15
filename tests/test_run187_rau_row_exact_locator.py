import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/rau_2019_row_level_exact_locator_run187_2026-09-11.json"
SEARCH = ROOT / "data/source_census/search_log_run187.jsonl"
STATUS = ROOT / "status/mlhkp_progress.json"


def test_run187_rau_exact_locator_and_integrity_boundary():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["source"]["doi"] == "10.5281/zenodo.3380874"
    assert d["source"]["manifestation"] == "pMunda_cognate_set_2019-08-29.csv"
    assert d["source"]["license"] == "CC0-1.0"
    assert d["verification"]["authoritative_plaintext_manifestation_verified"] is True
    assert d["verification"]["independent_checksum_recomputed"] is False
    row = d["exact_locator_evidence"][0]
    assert row["record_id"] == "#A0001"
    assert "mu_form 'da:'" in row["source_attributed_observation"]
    assert "mu_source 'BMED.p31'" in row["source_attributed_observation"]
    assert d["ingestion_decision"]["exact_locator_record_promoted"] is True
    assert d["ingestion_decision"]["lexical_rows_copied_into_cultural_or_language_corpus"] is False
    assert d["ingestion_decision"]["evidence_graph_node_added"] is False
    assert d["rights_and_cultural_governance"]["license_extended_to_underlying_historical_sources"] is False
    assert d["rights_and_cultural_governance"]["participant_consent_inferred"] is False
    assert d["rights_and_cultural_governance"]["community_validation_inferred"] is False
    assert d["rights_and_cultural_governance"]["cultural_access_permission_inferred"] is False


def test_run187_search_covers_all_requested_classes():
    rows = [json.loads(line) for line in SEARCH.read_text(encoding="utf-8").splitlines() if line.strip()]
    summary = rows[0]
    required = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert required.issubset(set(summary["classes"]))
    assert summary["search_id"] == "MMSC-SEARCH-000187"


def test_run187_count_contract_stays_noninflated():
    s = json.loads(STATUS.read_text(encoding="utf-8"))
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
