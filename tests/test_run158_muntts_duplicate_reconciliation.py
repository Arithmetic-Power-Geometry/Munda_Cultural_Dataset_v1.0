from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_web_mun_0090_reconciles_to_existing_muntts_identity_without_count_inflation():
    web = load("data/source_census/web_discovery_expansion_2026-09-10_run22.json")["records"][0]
    discoveries = load("data/source_census/mmsc_discoveries.json")["records"]
    mmsc = load("data/source_census/mmsc_index.json")
    audit = load("data/source_census/muntts_duplicate_reconciliation_run158_2026-09-10.json")

    src = next(r for r in discoveries if r["source_id"] == "SRC-MMSC-000012")
    assert src["identifier"] == {"scheme": "DOI", "value": "10.18653/v1/2024.computel-1.11"}
    assert web["doi"] == src["identifier"]["value"]
    assert web["title"] == src["title"]
    assert web["canonicalization"]["status"] == "duplicate_existing_permanent_identity"
    assert web["canonicalization"]["canonical_source_id"] == "SRC-MMSC-000012"

    mm = mmsc["metrics"]
    assert mm["web_discovery_records_observed"] == 90
    assert mm["web_discovery_unique_leads"] == 87
    assert mm["web_discovery_duplicate_records"] == 3
    assert mm["web_discovery_leads_counted_in_audited_identity_total"] == 13
    assert mm["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 74
    assert mm["sources_discovered"] == 41
    assert mmsc["latest_duplicate_reconciliation"]["web_source_id"] == "WEB-MUN-0090"
    assert audit["decision"] == "duplicate_existing_permanent_identity"


def test_run158_preserves_rights_consent_and_cultural_access_boundaries():
    audit = load("data/source_census/muntts_duplicate_reconciliation_run158_2026-09-10.json")
    boundary = audit["rights_and_governance_boundary"]
    assert boundary["paper_identity_reconciliation_changes_content_entitlement"] is False
    assert boundary["participant_audio_ingested"] is False
    assert boundary["participant_transcripts_ingested"] is False
    assert boundary["consent_inferred"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_overrides_entitlement"] is True
