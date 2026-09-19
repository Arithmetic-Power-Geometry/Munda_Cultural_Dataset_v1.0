from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/web_mun_0086_canonicalization_run169_2026-09-10.json"
MMSC = ROOT / "data/source_census/mmsc_index.json"
DISCOVERIES = ROOT / "data/source_census/mmsc_discoveries.json"
METRICS = ROOT / "publication/generated/release_metrics.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run169_web_0086_is_canonicalized_once_with_synced_counts():
    audit = load(AUDIT)
    mmsc = load(MMSC)
    discoveries = load(DISCOVERIES)["records"]
    metrics = load(METRICS)
    assert audit["web_source_id"] == "WEB-MUN-0086"
    assert audit["decision"]["canonical_source_id"] == "SRC-MMSC-000016"
    assert audit["decision"]["dedupe_key"] == "doi:10.1177/23210249221127832"
    assert [r["source_id"] for r in discoveries] == [f"SRC-MMSC-{i:06d}" for i in range(1, 17)]
    src = discoveries[-1]
    assert src["identifier"] == {"scheme": "DOI", "value": "10.1177/23210249221127832"}
    assert src["edition_relationships"] == [{"relationship": "discovery_lead", "identifier": "WEB-MUN-0086"}]
    assert mmsc["metrics"]["sources_discovered"] == 42
    assert mmsc["metrics"]["standalone_mmsc_discoveries"] == 16
    assert mmsc["metrics"]["web_discovery_leads_counted_in_audited_identity_total"] == 14
    assert mmsc["metrics"]["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 73
    assert metrics["sources_discovered"] == 42
    assert metrics["web_discovery_leads_counted_in_audited_identity_total"] == 14
    assert metrics["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 73


def test_run169_preserves_scope_rights_and_cultural_access_boundaries():
    audit = load(AUDIT)
    src = load(DISCOVERIES)["records"][-1]
    boundary = audit["munda_scope_boundary"]
    rights = audit["rights_governance"]
    effect = audit["evidence_effect"]
    assert boundary["exact_munda_specific_passage_verified"] is False
    assert boundary["munda_specific_factual_claim_promoted"] is False
    assert boundary["restricted_full_text_ingested"] is False
    assert boundary["participant_derived_content_ingested"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_inferred"] is False
    assert rights["public_abstract_is_not_full_text_permission"] is True
    assert rights["copyright_entitlement_does_not_override_cultural_access"] is True
    assert effect["claims_added"] == effect["evidence_records_added"] == effect["evidence_links_added"] == 0
    assert src["evidence_link_state"] == "not_linked_no_munda_specific_passage_verified"
