import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    with open(ROOT / path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def test_run159_bnf_exact_locator_boundary():
    rec = load_json("data/source_census/bnf_durang_kahani_audio_exact_locator_run159_2026-09-10.json")
    assert rec["run"] == 159
    assert rec["raw_discovery_id"] == "WEB-MUN-0020"
    assert rec["catalogue_identifier"]["ark"] == "ark:/12148/cb42562690s"
    assert rec["catalogue_identifier"]["frbnf"] == "FRBNF42562690"
    assert rec["catalogue_exact_locators"]["matrix_number"] == "3306Y"
    assert rec["catalogue_exact_locators"]["digital_holding"] == "NUMAUD-130038"
    assert rec["catalogue_exact_locators"]["recording_place_year"] == "Ranchi, 1914"
    assert rec["rights_access_consent"]["audio_reuse_permission_verified"] is False
    assert rec["rights_access_consent"]["performer_consent_for_secondary_reuse_verified"] is False
    assert rec["rights_access_consent"]["community_validation_verified"] is False
    assert rec["rights_access_consent"]["cultural_access_clearance_verified"] is False
    assert rec["rights_access_consent"]["redistribution_allowed_by_mlhkp"] is False
    assert rec["evidence_promotion"]["claim_count_change"] == 0
    assert rec["evidence_promotion"]["evidence_graph_count_change"] == 0


def test_run159_counts_stay_audited_and_stable():
    idx = load_json("data/source_census/mmsc_index.json")
    m = idx["metrics"]
    assert m["sources_discovered"] == 41
    assert m["web_discovery_records_observed"] == 90
    assert m["web_discovery_unique_leads"] == 87
    assert m["web_discovery_duplicate_records"] == 3
    assert m["web_discovery_leads_counted_in_audited_identity_total"] == 13
    assert m["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 74
