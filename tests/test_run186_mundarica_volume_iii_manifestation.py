import json
from pathlib import Path


def _load():
    p = Path("data/source_census/mundarica_volume_iii_secondary_manifestation_run186_2026-09-11.json")
    return json.loads(p.read_text(encoding="utf-8"))


def test_run186_volume_iii_secondary_manifestation_is_non_promotional():
    d = _load()
    m = d["secondary_digitized_manifestation"]
    a = d["mundarica_release_accounting"]
    e = d["evidence_boundary"]
    r = d["rights_and_cultural_access"]

    assert d["branch"] == "mlhkp-v2"
    assert d["run"] == 186
    assert m["item_identifier"] == "in.ernet.dli.2015.14921"
    assert m["catalogued_total_pages"] == 264
    assert m["manifestation_hash_verified"] is False
    assert m["authoritative_release_scan"] is False
    assert a["volume"] == "III"
    assert a["authoritative_scans_registered_delta"] == 0
    assert a["verified_complete_volumes_delta"] == 0
    assert a["ocr_promoted_to_verified_transcription"] is False
    assert e["cultural_passages_ingested"] is False
    assert e["ocr_text_ingested_as_verified"] is False
    assert e["page_level_cultural_claim_promoted"] is False
    assert e["evidence_graph_count_changed"] is False
    assert e["source_identity_count_changed"] is False
    assert r["repository_rights_label_treated_as_independently_adjudicated_rights"] is False
    assert r["repository_download_visibility_treated_as_reuse_permission"] is False
    assert r["community_validation_inferred"] is False
    assert r["cultural_access_inferred"] is False
    assert r["cultural_access_overrides_technical_or_repository_availability"] is True
