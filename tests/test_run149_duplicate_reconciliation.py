from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_run149_duplicate_reconciliation_is_count_safe():
    mmsc = load("data/source_census/mmsc_index.json")
    run20 = load("data/source_census/web_discovery_expansion_2026-09-10_run20.json")
    audit = load("data/source_census/run149_deterministic_duplicate_reconciliation_2026-09-10.json")

    record = run20["records"][0]
    assert record["id"] == "WEB-MUN-0088"
    assert record["canonicalization"]["status"] == "canonicalized_duplicate_web_lead"
    assert record["canonicalization"]["canonical_web_source_id"] == "WEB-MUN-0032"

    metrics = mmsc["metrics"]
    assert metrics["web_discovery_records_observed"] == 88
    assert metrics["web_discovery_unique_leads"] == 87
    assert metrics["web_discovery_duplicate_records"] == 1
    assert metrics["web_discovery_leads_counted_in_audited_identity_total"] == 13
    assert metrics["web_discovery_unique_leads_remaining_outside_audited_identity_total"] == 74
    assert metrics["sources_discovered"] == 41

    effect = audit["count_effect"]
    assert effect["claims"] == effect["evidence_records"] == effect["evidence_links"] == 52
    assert audit["cultural_claims_added"] == 0


def test_mullick_is_existing_web_lead_not_new_id():
    audit = load("data/source_census/run149_deterministic_duplicate_reconciliation_2026-09-10.json")
    mullick = audit["findings"][0]
    assert mullick["identifier"] == "doi:10.1177/097185240000400301"
    assert mullick["canonical_web_source_id"] == "WEB-MUN-0081"
    assert mullick["decision"] == "existing_lead_not_new"
