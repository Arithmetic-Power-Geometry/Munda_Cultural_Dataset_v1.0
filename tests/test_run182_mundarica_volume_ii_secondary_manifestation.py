from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'data' / 'source_census' / 'mundarica_volume_ii_secondary_manifestation_run182_2026-09-11.json'
MMSC = ROOT / 'data' / 'source_census' / 'mmsc_index.json'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def test_run182_mundarica_ii_secondary_manifestation_is_exact_and_bounded():
    audit = load(AUDIT)
    assert audit['run'] == 182
    assert audit['branch'] == 'mlhkp-v2'
    m = audit['secondary_digitized_manifestation']
    assert m['item_identifier'] == 'dli.bengal.10689.21001'
    assert m['upstream_source_handle'] == 'http://hdl.handle.net/10689/21001'
    assert m['catalogued_total_pages'] == 406
    assert m['scanning_centre'] == 'C-DAC KOLKATA'
    assert m['ocr_engine_as_catalogued'] == 'ABBYY FineReader 11.0 (Extended OCR)'
    assert m['authoritative_release_scan'] is False
    assert m['manifestation_page_images_independently_compared_to_physical_authoritative_copy'] is False
    assert m['manifestation_hash_verified'] is False


def test_run182_does_not_promote_ocr_rights_or_cultural_access():
    audit = load(AUDIT)
    a = audit['mundarica_release_accounting']
    r = audit['rights_and_cultural_access']
    e = audit['evidence_boundary']
    assert a['authoritative_scans_registered_delta'] == 0
    assert a['verified_complete_volumes_delta'] == 0
    assert a['ocr_promoted_to_verified_transcription'] is False
    assert r['repository_download_visibility_treated_as_reuse_permission'] is False
    assert r['copyright_or_public_domain_status_inferred'] is False
    assert r['community_validation_inferred'] is False
    assert r['cultural_access_inferred'] is False
    assert r['cultural_access_overrides_technical_availability'] is True
    assert e['cultural_passages_ingested'] is False
    assert e['ocr_text_ingested_as_verified'] is False
    assert e['page_level_cultural_claim_promoted'] is False
    assert e['evidence_graph_count_changed'] is False
    assert e['source_identity_count_changed'] is False


def test_run182_mmsc_counts_remain_stable_for_non_count_bearing_manifestation_audit():
    mmsc = load(MMSC)['metrics']
    assert mmsc['sources_discovered'] == 42
    assert mmsc['web_discovery_records_observed'] == 90
    assert mmsc['web_discovery_unique_leads'] == 87
    assert mmsc['web_discovery_duplicate_records'] == 3
    assert mmsc['web_discovery_leads_counted_in_audited_identity_total'] == 14
    assert mmsc['web_discovery_unique_leads_remaining_outside_audited_identity_total'] == 73
