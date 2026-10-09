import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "lsi_west_bengal_mundari_primary_page_locator_run296_2026-09-13.json"
LOG = ROOT / "data" / "source_census" / "search_log_run296.jsonl"


def test_run296_primary_locator_and_governance_boundary():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["run_id"] == 296
    assert data["canonical_work"]["official_pdf_url"].endswith("/LSI_WB_PART_I.pdf")
    assert data["canonical_work"]["target_section"] == "MUNDARI"
    assert data["canonical_work"]["exact_printed_page_locator"] == 391
    assert data["verified_from_first_party_pdf_surface"]["direct_official_pdf_resolves"] is True
    assert data["integrity_state"]["independent_pdf_byte_acquisition_completed"] is False
    assert data["integrity_state"]["sha256_independently_recomputed"] is False
    assert data["fieldwork_governance_boundary"]["participant_derived_source"] is True
    assert data["fieldwork_governance_boundary"]["elicited_language_forms_promoted"] is False
    assert data["fieldwork_governance_boundary"]["cultural_claims_promoted"] is False
    assert data["fieldwork_governance_boundary"]["participant_consent_inferred"] is False
    assert data["fieldwork_governance_boundary"]["community_validation_inferred"] is False
    assert data["fieldwork_governance_boundary"]["cultural_access_permission_inferred"] is False
    assert data["promotion"]["new_controlled_claims"] == 0
    assert data["promotion"]["new_controlled_evidence_records"] == 0
    assert data["promotion"]["new_evidence_links"] == 0
    assert data["deduplication"]["unresolved_WEB_MUN_count_decrement"] == 0


def test_run296_all_controlled_census_classes_logged_once():
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    expected = {
        "books", "dictionaries", "grammars", "peer_reviewed_articles",
        "theses_dissertations", "government_TRI_Census_LSI", "archives",
        "newspapers_periodicals", "web_resources", "datasets", "audio",
        "video", "maps", "relevant_media",
    }
    assert len(rows) == 14
    assert {row["class"] for row in rows} == expected
    assert len({row["search_id"] for row in rows}) == 14
    assert all(row["run_id"] == 296 for row in rows)
