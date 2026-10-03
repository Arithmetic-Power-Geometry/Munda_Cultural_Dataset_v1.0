import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/proietti_2025_rights_resolution_run180_2026-09-11.json"


def test_proietti_rights_boundary_is_explicit_and_non_promotional():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    rights = data["rights_resolution"]
    promotion = data["promotion"]

    assert data["run"] == 180
    assert rights["exact_cc_variant_verified"] is False
    assert rights["redistribution_permission_verified"] is False
    assert rights["participant_consent_inferred"] is False
    assert rights["community_validation_inferred"] is False
    assert rights["cultural_access_permission_inferred"] is False
    assert data["manifestation_verification"]["pdf_bytes_acquired"] is False
    assert data["manifestation_verification"]["page_level_passages_verified"] is False
    assert promotion == {
        "source_identities_added": 0,
        "claims_added": 0,
        "evidence_records_added": 0,
        "evidence_links_added": 0,
        "full_text_passages_ingested": 0,
        "participant_records_ingested": 0,
        "counts_changed": False,
    }
