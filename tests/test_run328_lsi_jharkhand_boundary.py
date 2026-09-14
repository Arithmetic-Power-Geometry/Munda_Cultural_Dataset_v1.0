import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_census" / "lsi_jharkhand_mundari_distribution_locator_run328_2026-09-14.json"
LOG = ROOT / "data" / "source_census" / "search_log_run328.jsonl"


def test_run328_lsi_boundary_and_14_class_refresh():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["source"]["first_party"] is True
    assert data["source"]["pdf_url"].endswith("LSI_JHARKHAND.pdf")
    boundary = data["evidence_boundary"]
    assert boundary["numeric_evidence_promoted_to_controlled_graph_this_run"] is False
    assert boundary["cultural_claims_promoted"] is False
    assert boundary["participant_consent_inferred"] is False
    assert boundary["community_validation_inferred"] is False
    assert boundary["cultural_access_authorization_inferred"] is False
    retry = data["retry_state"]
    assert retry["independent_hash_verified"] is False
    assert retry["page_image_verified"] is False
    assert retry["page_number_verified"] is False

    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 14
    assert len({row["class"] for row in rows}) == 14
    assert all(row["search_id"] == "MMSC-SEARCH-000328" for row in rows)
    assert not any(row["promoted"] for row in rows)
