import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_run155_muntts_identity_and_locator_contract():
    expansion = load("data/source_census/web_discovery_expansion_2026-09-10_run22.json")
    rec = expansion["records"][0]
    assert rec["id"] == "WEB-MUN-0090"
    assert rec["doi"] == "10.18653/v1/2024.computel-1.11"
    assert rec["canonicalization"]["status"] == "new_unique_web_lead_pending_master_identity_reconciliation"

    locator = load("data/source_census/muntts_2024_mundari_dataset_methods_exact_locator_run155_2026-09-10.json")
    assert locator["web_source_id"] == "WEB-MUN-0090"
    assert locator["rights_access_consent_boundary"]["audio_transcripts_ingested"] is False
    assert locator["rights_access_consent_boundary"]["community_validation_claimed"] is False
    assert len(locator["verified_locators"]) >= 4


def test_run155_mmsc_count_contract():
    mmsc = load("data/source_census/mmsc_index.json")
    mm = mmsc["metrics"]
    assert mm["web_discovery_records_observed"] == 90
    assert mm["web_discovery_unique_leads"] == 88
    assert mm["web_discovery_duplicate_records"] == 2
    assert mm["web_discovery_leads_counted_in_audited_identity_total"] == 13
    assert mm["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 75
    assert mm["sources_discovered"] == 41
