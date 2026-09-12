import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/source_census/saboo_2020_munda_land_inheritance_exact_locator_run185_2026-09-11.json"


def test_run185_saboo_identity_and_metadata():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert d["run"] == 185
    assert d["branch"] == "mlhkp-v2"
    assert d["source"]["doi"] == "10.1177/0019556120982196"
    assert d["source"]["journal"] == "Indian Journal of Public Administration"
    assert d["source"]["volume"] == "66"
    assert d["source"]["issue"] == "4"
    assert d["source"]["pages"] == "552-562"
    assert d["source"]["first_published_online"] == "2021-01-20"
    assert d["scope_classification"]["munda_specific"] is True
    assert d["scope_classification"]["jharkhand_specific"] is True
    assert d["evidence_promotion"]["discovery_only"] is False
    assert d["evidence_promotion"]["exact_locator_metadata_record_created"] is True


def test_run185_saboo_restricted_access_and_no_cultural_overclaim():
    d = json.loads(AUDIT.read_text(encoding="utf-8"))
    g = d["rights_access_consent_cultural_uncertainty"]
    assert g["publisher_marks_restricted_access"] is True
    assert g["publisher_requests_permissions"] is True
    assert g["open_license_verified"] is False
    assert g["full_text_lawfully_obtained_in_run185"] is False
    assert g["participant_or_fieldwork_content_ingested"] is False
    assert g["cultural_claims_ingested"] is False
    assert g["community_validation_inferred"] is False
    assert g["participant_consent_inferred"] is False
    assert g["cultural_access_permission_inferred"] is False
    assert d["deduplication"]["count_bearing_registration_performed"] is False
    assert d["evidence_promotion"]["new_cultural_claims"] == 0
    assert d["evidence_promotion"]["new_participant_records"] == 0
    assert d["evidence_promotion"]["evidence_graph_change"] == "none"
